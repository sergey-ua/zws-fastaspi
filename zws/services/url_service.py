package zws.services

import pydantic
from pydantic import BaseModel, validator
from url_repository import UrlRepository
from typing import Optional
import logging

class UrlInfo(BaseModel):
    short_url: str
    long_url: str

    @validator('short_url')
    def validate_short_url(cls, v):
        if len(v) <= 0 or len(v) >= 100:
            raise ValueError('Short URL must be between 1 and 100 characters')
        return v

    @validator('long_url')
    def validate_long_url(cls, v):
        if len(v) <= 0 or len(v) >= 2000:
            raise ValueError('Long URL must be between 1 and 2000 characters')
        return v

class UrlService:
    def __init__(self, url_repository: UrlRepository):
        self.url_repository = url_repository
        self.logger = logging.getLogger(__name__)

    def validate_short_url(self, short_url: str) -> bool:
        try:
            UrlInfo(short_url=short_url, long_url='')
            return True
        except ValueError:
            return False

    def parse_short_url(self, short_url: str) -> Optional[UrlInfo]:
        if not self.validate_short_url(short_url):
            return None
        try:
            return self.url_repository.get_url_info(short_url)
        except Exception as e:
            self.logger.error(f'Error parsing short URL: {e}')
            return None

    def transform_long_url(self, long_url: str) -> str:
        return long_url.strip()

    def validate_long_url(self, long_url: str) -> bool:
        try:
            UrlInfo(short_url='', long_url=long_url)
            return True
        except ValueError:
            return False

    def detect_captcha_phishing(self, long_url: str) -> bool:
        suspicious_keywords = ["captcha", "phishing", "verify", "login"]
        suspicious_tlds = [".ru", ".cn", ".biz"]
        for keyword in suspicious_keywords:
            if keyword in long_url.lower():
                return True
        for tld in suspicious_tlds:
            if long_url.lower().endswith(tld):
                return True
        return False

    def create_short_url(self, long_url: str) -> Optional[str]:
        if not self.validate_long_url(long_url):
            self.logger.error(f'Invalid long URL: {long_url}')
            return None
        if self.detect_captcha_phishing(long_url):
            self.logger.error(f'Suspicious long URL: {long_url}')
            return None
        transformed_long_url = self.transform_long_url(long_url)
        try:
            short_url = self.url_repository.create_short_url(transformed_long_url)
            return short_url
        except Exception as e:
            self.logger.error(f'Error creating short URL: {e}')
            return None

    def get_long_url(self, short_url: str) -> Optional[str]:
        url_info = self.parse_short_url(short_url)
        if url_info is None:
            self.logger.error(f'Invalid short URL: {short_url}')
            return None
        return url_info.long_url

    def delete_short_url(self, short_url: str) -> bool:
        try:
            self.url_repository.delete_short_url(short_url)
            return True
        except Exception as e:
            self.logger.error(f'Error deleting short URL: {e}')
            return False

    def update_long_url(self, short_url: str, new_long_url: str) -> bool:
        if not self.validate_long_url(new_long_url):
            self.logger.error(f'Invalid new long URL: {new_long_url}')
            return False
        if self.detect_captcha_phishing(new_long_url):
            self.logger.error(f'Suspicious new long URL: {new_long_url}')
            return False
        try:
            self.url_repository.update_long_url(short_url, new_long_url)
            return True
        except Exception as e:
            self.logger.error(f'Error updating long URL: {e}')
            return False