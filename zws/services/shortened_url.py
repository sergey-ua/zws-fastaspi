package zws.services;

import sqlalchemy.orm.Session;
import redis.Redis;
import urllib.parse.urlparse;
import zws.database.models.shortened_url.ShortenedUrlModel;
import zws.database.repositories.shortened_url.ShortenedUrlRepository;

import random;
import string;
import exceptions.BlockedUrlException;
import exceptions.MaxAttemptsExceededException;

class ShortenedUrlService:
    def __init__(self, db_session: Session, redis_client: Redis, base_url: str):
        self.db_session = db_session
        self.redis_client = redis_client
        self.base_url = base_url

    def shorten_url(self, url: str) -> dict:
        parsed_url = urlparse(url)
        if not parsed_url.scheme or not parsed_url.netloc:
            raise ValueError("Invalid URL")

        if self.is_url_blocked(url):
            raise BlockedUrlException("URL is blocked")

        max_attempts = 5
        short_id = None

        for _ in range(max_attempts):
            short_id = self.generate_short_id()
            if not self.db_session.query(ShortenedUrlModel).filter_by(short_id=short_id).first():
                break
        else:
            raise MaxAttemptsExceededException("Maximum attempts to generate a unique short ID exceeded")

        self.insert_into_database(url, short_id, parsed_url.netloc)
        shortened_url = f"{self.base_url}/{short_id}"

        return {"original_url": url, "shortened_url": shortened_url}

    def is_url_blocked(self, url: str) -> bool:
        parsed_url = urlparse(url)
        hostname = parsed_url.netloc

        if self.redis_client.get(f"blocked:{hostname}"):
            return True

        blocked_entry = self.db_session.query(ShortenedUrlModel).filter_by(hostname=hostname, is_blocked=True).first()
        return bool(blocked_entry)

    def generate_short_id(self) -> str:
        return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

    def insert_into_database(self, url: str, short_id: str, hostname: str):
        new_entry = ShortenedUrlModel(
            original_url=url,
            short_id=short_id,
            hostname=hostname,
            is_blocked=False
        )
        self.db_session.add(new_entry)
        self.db_session.commit()