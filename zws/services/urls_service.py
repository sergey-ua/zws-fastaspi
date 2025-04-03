package zws.services

from sqlalchemy.exc import IntegrityError
from zws.database.repositories import UrlRepository
from zws.database.models.blocked_hostname import BlockedHostname
from zws.exceptions import UnprocessableEntityException, InternalServerErrorException
from zws.utils import generate_short_id, to_base64, is_url_blocked
from urllib.parse import urlparse
import asyncio
import aioredis

class UrlsService:
    def __init__(self, url_repository: UrlRepository, redis_client: aioredis.Redis):
        self.url_repository = url_repository
        self.redis_client = redis_client

    async def shorten_url(self, long_url: str) -> dict:
        url_object = urlparse(long_url)

        if await is_url_blocked(url_object, self.redis_client):
            raise UnprocessableEntityException('That URL hostname is blocked')

        MAX_SHORT_ID_GENERATION_ATTEMPTS = 5
        attempts = 0
        while attempts < MAX_SHORT_ID_GENERATION_ATTEMPTS:
            short_id = generate_short_id()
            base64_short_id = to_base64(short_id)
            try:
                await self.url_repository.insert_url(url_object, base64_short_id)
                return {'short': base64_short_id, 'url': long_url}
            except IntegrityError as e:
                if e.orig.pgcode == '23505':
                    attempts += 1
                    continue
                else:
                    raise InternalServerErrorException('Database error occurred')
        raise InternalServerErrorException('Unable to generate a unique short ID within the max number of attempts')