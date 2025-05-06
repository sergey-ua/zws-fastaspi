package zws.database.repositories

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from pydantic import BaseModel, validator
from typing import List, Optional
from datetime import datetime
from zws.database.base_repository import BaseRepository
from zws.database.exceptions import DatabaseException

SQLALCHEMY_DATABASE_URL = "sqlite:///url_stats.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class UrlStats(Base):
    __tablename__ = "url_stats"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, unique=True, index=True)
    stats = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)

class UrlStatsModel(BaseModel):
    url: str
    stats: str

    class Config:
        orm_mode = True

    @validator('url')
    def url_must_not_be_empty(cls, v):
        if not v:
            raise ValueError('URL must not be empty')
        return v

    @validator('stats')
    def stats_must_be_string(cls, v):
        if not isinstance(v, str):
            raise ValueError('Stats must be a string')
        if not v:
            raise ValueError('Stats must not be empty')
        return v

class UrlStatsRepository(BaseRepository):
    def __init__(self, session):
        super().__init__(session)

    def get_url_stats(self, url: str) -> Optional[UrlStats]:
        try:
            if not url:
                raise ValueError('URL must not be empty')
            result = self.session.query(UrlStats).filter(UrlStats.url == url).all()
            if len(result) > 1:
                raise ValueError("Multiple URL stats found")
            return result[0] if result else None
        except ValueError as e:
            raise ValueError("Invalid URL or multiple URL stats found") from e
        except Exception as e:
            raise DatabaseException("Failed to retrieve URL stats") from e

    def create_url_stats(self, url_stats_model: UrlStatsModel) -> UrlStats:
        try:
            if not isinstance(url_stats_model, UrlStatsModel):
                raise ValueError('URL stats model must be an instance of UrlStatsModel')
            if not url_stats_model:
                raise ValueError('URL stats model must not be empty')
            existing_url_stats = self.get_url_stats(url_stats_model.url)
            if existing_url_stats:
                raise ValueError("URL stats already exist")
            url_stats = UrlStats(url=url_stats_model.url, stats=url_stats_model.stats)
            self.session.begin()
            self.session.add(url_stats)
            self.session.commit()
            self.session.refresh(url_stats)
            return url_stats
        except ValueError as e:
            self.session.rollback()
            raise ValueError("Invalid URL stats model or URL stats already exist") from e
        except Exception as e:
            self.session.rollback()
            raise DatabaseException("Failed to create URL stats") from e

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()