package zws.services;

import urllib.parse
from zws.database.repositories.shortened_url_repository import ShortenedUrlRepository
import uuid

class ShortenedUrlService:
    def __init__(self):
        self.repository = ShortenedUrlRepository()

    def shorten_url(self, url):
        parsed_url = urllib.parse.urlparse(url)
        if not parsed_url.scheme or not parsed_url.netloc:
            raise ValueError("Invalid URL")
        short_identifier = self._generate_short_identifier()
        self.repository.create_shortened_url(original_url=url, short_identifier=short_identifier)
        return {"original_url": url, "shortened_url": short_identifier}

    def get_shortened_url(self, short):
        record = self.repository.get_shortened_url_by_short(short_identifier=short)
        if not record:
            raise ValueError("Shortened URL not found")
        return record

    def list_shortened_urls(self):
        return self.repository.get_all_shortened_urls()

    def _generate_short_identifier(self):
        return uuid.uuid4().hex[:8]