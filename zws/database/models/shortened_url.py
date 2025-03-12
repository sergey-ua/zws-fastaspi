package zws.database.models

from pydantic import BaseModel
from sqlalchemy import Column, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from zws.database.repositories import Session
from base64 import b64encode, b64decode
import os
import logging
from typing import Optional

Base = declarative_base()
logger = logging.getLogger(__name__)

class ShortenedUrl(BaseModel):
    code: str
    original_url: str
    blocked: bool

    class Config:
        orm_mode = True

class ShortenedUrlModel(Base):
    __tablename__ = 'shortened_urls'
    code = Column(String, primary_key=True)
    original_url = Column(String)
    blocked = Column(Boolean)

    def encode_code(self):
        try:
            return b64encode(self.code.encode()).decode()
        except Exception as e:
            logger.error(f"Failed to encode code: {e}")
            raise

    @classmethod
    def get_by_code(cls, session: Session, code: str) -> Optional['ShortenedUrlModel']:
        try:
            return session.query(cls).filter_by(code=code).first()
        except Exception as e:
            logger.error(f"Failed to retrieve URL by code: {e}")
            raise

    @classmethod
    def get_url_and_blocked_status(cls, session: Session, code: str) -> Optional[tuple]:
        try:
            shortened_url = session.query(cls).filter_by(code=code).first()
            if shortened_url:
                return shortened_url.original_url, shortened_url.blocked
            else:
                return None
        except Exception as e:
            logger.error(f"Failed to retrieve URL and blocked status: {e}")
            raise

    @classmethod
    def get_url(cls, session: Session, code: str) -> Optional[str]:
        try:
            shortened_url = session.query(cls).filter_by(code=code).first()
            if shortened_url:
                return shortened_url.original_url
            else:
                return None
        except Exception as e:
            logger.error(f"Failed to retrieve URL: {e}")
            raise

    @classmethod
    def get_blocked_status(cls, session: Session, code: str) -> Optional[bool]:
        try:
            shortened_url = session.query(cls).filter_by(code=code).first()
            if shortened_url:
                return shortened_url.blocked
            else:
                return None
        except Exception as e:
            logger.error(f"Failed to retrieve blocked status: {e}")
            raise