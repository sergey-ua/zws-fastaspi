package zws.services

import urllib.parse
import random
import string
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from zws.database.repositories.url_repository import UrlRepository
from zws.config import ConfigService
from redis import Redis

class BlockedUrlException(Exception):
    pass

class ShortIdGenerationException(Exception):
    pass

class UrlsService:
    def __init__(self, db_session: AsyncSession, redis_client: Redis, config_service: ConfigService):
        self.db_session = db_session
        self.redis_client = redis_client
        self.config_service = config_service
        self.url_repository = UrlRepository(db_session)

    async def shorten_url(self, long_url: str) -> dict:
        parsed_url = urllib.parse.urlparse(long_url)
        if not parsed_url.scheme or not parsed_url.netloc:
            raise ValueError("Invalid URL")

        if await self.is_url_blocked(long_url):
            raise BlockedUrlException("The URL is blocked")

        max_attempts = 5
        short_id = None

        for _ in range(max_attempts):
            short_id = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
            if not await self.url_repository.is_short_id_exists(short_id):
                break
        else:
            raise ShortIdGenerationException("Failed to generate a unique short ID")

        try:
            await self.url_repository.insert_url_mapping(long_url, short_id)
        except SQLAlchemyError:
            await self.db_session.rollback()
            raise

        base_url = self.config_service.get("BASE_URL")
        short_url = f"{base_url}/{short_id}"
        return {"short": short_id, "url": short_url}

    async def is_url_blocked(self, url: str) -> bool:
        hostname = urllib.parse.urlparse(url).hostname
        if not hostname:
            raise ValueError("Invalid URL")

        cached_result = self.redis_client.get(hostname)
        if cached_result is not None:
            return cached_result == b"1"

        try:
            is_blocked = await self.url_repository.is_hostname_blocked(hostname)
        except SQLAlchemyError:
            await self.db_session.rollback()
            raise

        self.redis_client.set(hostname, "1" if is_blocked else "0", ex=3600)
        return is_blocked