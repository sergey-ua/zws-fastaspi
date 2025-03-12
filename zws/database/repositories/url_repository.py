package zws.database.repositories

from zws.database.models import Url
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from typing import Optional
import logging

class UrlRepository:
    def __init__(self, db_session):
        self.db_session = db_session
        self.logger = logging.getLogger(__name__)

    def get_url_by_short_base64(self, short_base64: str) -> Optional[Url]:
        try:
            if not short_base64:
                self.logger.error("Short base64 is empty")
                return None
            return self.db_session.query(Url).filter(Url.short_base64 == short_base64).first()
        except Exception as e:
            self.logger.error(f"Error getting URL by short base64: {e}")
            return None

    def create_url(self, url: Url) -> None:
        try:
            if not url:
                self.logger.error("URL is empty")
                return
            self.db_session.add(url)
            self.db_session.commit()
        except Exception as e:
            self.logger.error(f"Error creating URL: {e}")
            self.db_session.rollback()