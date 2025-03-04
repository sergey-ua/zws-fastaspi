package zws.services

import sqlalchemy as db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel, validator
from zws.services import blocked_hostnames_service
from contextlib import contextmanager
from sqlalchemy.exc import SQLAlchemyError
from zws.services import dependency_injector
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from urllib.parse import urlparse
from zws.services.dependency_injector import inject

Base = declarative_base()

class ShortUrl(Base):
    __tablename__ = 'short_urls'
    id = Column(Integer, primary_key=True)
    short_url = Column(String)
    long_url = Column(String)

class ShortUrlRepository:
    def __init__(self, db_url):
        self.engine = create_engine(db_url)
        self.Session = sessionmaker(bind=self.engine)

    @contextmanager
    def session(self):
        session = self.Session()
        try:
            yield session
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def get_short_url(self, short_url):
        with self.session() as session:
            return session.query(ShortUrl).filter(ShortUrl.short_url == short_url).first()

class BlockedHostnamesService:
    def __init__(self, blocked_hostnames):
        self.blocked_hostnames = set(blocked_hostnames)

    def add_blocked_hostname(self, hostname):
        self.blocked_hostnames.add(hostname)

    def is_blocked(self, url):
        hostname = urlparse(url).hostname
        return hostname in self.blocked_hostnames

class ShortUrlModel(BaseModel):
    short_url: str

    @validator('short_url')
    def validate_short_url(cls, v):
        if not v:
            raise ValueError('Short URL is required')
        return v

class ShortUrlService:
    @inject
    def __init__(self, short_url_repository: ShortUrlRepository, blocked_hostnames_service: BlockedHostnamesService):
        self.short_url_repository = short_url_repository
        self.blocked_hostnames_service = blocked_hostnames_service

    def redirect(self, short_url_model: ShortUrlModel):
        try:
            short_url_info = self.short_url_repository.get_short_url(short_url_model.short_url)
            if short_url_info:
                if self.blocked_hostnames_service.is_blocked(short_url_info.long_url):
                    return "Error: URL is blocked"
                else:
                    return short_url_info.long_url
            else:
                return "Error: Short URL not found"
        except SQLAlchemyError as e:
            return f"Error: Database connection issue - {str(e)}"
        except Exception as e:
            return f"Error: Invalid input - {str(e)}"

import unittest
from unittest.mock import Mock

class TestShortUrlService(unittest.TestCase):
    def test_redirect(self):
        short_url_repository = Mock()
        short_url_repository.get_short_url.return_value = Mock(long_url='https://example.com')
        blocked_hostnames_service = Mock()
        blocked_hostnames_service.is_blocked.return_value = False
        short_url_service = ShortUrlService(short_url_repository, blocked_hostnames_service)
        short_url_model = ShortUrlModel(short_url='https://short.url')
        self.assertEqual(short_url_service.redirect(short_url_model), 'https://example.com')

    def test_redirect_blocked(self):
        short_url_repository = Mock()
        short_url_repository.get_short_url.return_value = Mock(long_url='https://example.com')
        blocked_hostnames_service = Mock()
        blocked_hostnames_service.is_blocked.return_value = True
        short_url_service = ShortUrlService(short_url_repository, blocked_hostnames_service)
        short_url_model = ShortUrlModel(short_url='https://short.url')
        self.assertEqual(short_url_service.redirect(short_url_model), 'Error: URL is blocked')

    def test_redirect_short_url_not_found(self):
        short_url_repository = Mock()
        short_url_repository.get_short_url.return_value = None
        blocked_hostnames_service = Mock()
        short_url_service = ShortUrlService(short_url_repository, blocked_hostnames_service)
        short_url_model = ShortUrlModel(short_url='https://short.url')
        self.assertEqual(short_url_service.redirect(short_url_model), 'Error: Short URL not found')

if __name__ == '__main__':
    unittest.main()