```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
from urllib.parse import urlparse
from typing import Optional
import uuid
import hashlib
from zws.models import UrlModel
from zws.services import BlockedHostnamesService

class UrlRepository:
    def __init__(self, session):
        self.session = session

    def get_url_by_shortened_url(self, shortened_url: str) -> Optional[UrlModel]:
        return self.session.query(UrlModel).filter(UrlModel.shortened_url == shortened_url).first()

    def create_url(self, original_url: str, shortened_url: str) -> UrlModel:
        url = UrlModel(original_url=original_url, shortened_url=shortened_url)
        self.session.add(url)
        self.session.commit()
        return url

    def get_url_by_original_url(self, original_url: str) -> Optional[UrlModel]:
        return self.session.query(UrlModel).filter(UrlModel.original_url == original_url).first()

class BlockedHostnamesService:
    def __init__(self):
        self.blocked_hostnames = set()

    def add_blocked_hostname(self, hostname: str):
        self.blocked_hostnames.add(hostname)

    def is_blocked(self, url: str) -> bool:
        hostname = urlparse(url).hostname
        return hostname in self.blocked_hostnames

class UrlService:
    def __init__(self, url_repository: UrlRepository, blocked_hostnames_service: BlockedHostnamesService):
        self.url_repository = url_repository
        self.blocked_hostnames_service = blocked_hostnames_service

    def shorten_url(self, original_url: str) -> str:
        try:
            if self.blocked_hostnames_service.is_blocked(original_url):
                raise ValueError("URL is blocked")
            existing_url = self.url_repository.get_url_by_original_url(original_url)
            if existing_url:
                return existing_url.shortened_url
            shortened_url = self.generate_shortened_url(original_url)
            existing_shortened_url = self.url_repository.get_url_by_shortened_url(shortened_url)
            if existing_shortened_url:
                raise ValueError("Shortened URL already exists")
            self.url_repository.create_url(original_url, shortened_url)
            return shortened_url
        except ValueError as e:
            raise ValueError(str(e))
        except Exception as e:
            raise Exception(f"An error occurred: {str(e)}")

    def get_original_url(self, shortened_url: str) -> str:
        try:
            url = self.url_repository.get_url_by_shortened_url(shortened_url)
            if url is None:
                raise ValueError("URL not found")
            return url.original_url
        except ValueError as e:
            raise ValueError(str(e))
        except Exception as e:
            raise Exception(f"An error occurred: {str(e)}")

    def is_url_blocked(self, url: str) -> bool:
        return self.blocked_hostnames_service.is_blocked(url)

    def generate_shortened_url(self, original_url: str) -> str:
        hashed_url = hashlib.sha256(original_url.encode()).hexdigest()[:6]
        return f"http://short.url/{hashed_url}"

def main():
    engine = create_engine('sqlite:///urls.db')
    Session = sessionmaker(bind=engine)
    session = Session()
    url_repository = UrlRepository(session)
    blocked_hostnames_service = BlockedHostnamesService()
    url_service = UrlService(url_repository, blocked_hostnames_service)
    original_url = "https://www.example.com"
    shortened_url = url_service.shorten_url(original_url)
    print(f"Shortened URL: {shortened_url}")
    print(f"Original URL: {url_service.get_original_url(shortened_url)}")
    print(f"Is URL blocked: {url_service.is_url_blocked(original_url)}")

if __name__ == "__main__":
    main()
```