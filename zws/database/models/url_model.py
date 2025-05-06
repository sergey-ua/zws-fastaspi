package zws.database.models

from pydantic import BaseModel, Field
from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from typing import Optional
import logging

Base = declarative_base()

class UrlStats(BaseModel):
    clicks: int = Field(0, ge=0)
    impressions: int = Field(0, ge=0)
    last_click: Optional[str] = Field(None)
    last_impression: Optional[str] = Field(None)

class UrlStatsModel(Base):
    __tablename__ = 'url_stats'
    id = Column(Integer, primary_key=True)
    url_id = Column(Integer, ForeignKey('urls.id'))
    clicks = Column(Integer)
    impressions = Column(Integer)
    last_click = Column(String)
    last_impression = Column(String)

    def to_pydantic(self) -> UrlStats:
        return UrlStats(
            clicks=self.clicks,
            impressions=self.impressions,
            last_click=self.last_click,
            last_impression=self.last_impression
        )

    @staticmethod
    def from_pydantic(stats: UrlStats):
        return UrlStatsModel(
            clicks=stats.clicks,
            impressions=stats.impressions,
            last_click=stats.last_click,
            last_impression=stats.last_impression
        )

class UrlModel(Base):
    __tablename__ = 'urls'
    id = Column(Integer, primary_key=True)
    url = Column(String)
    stats = relationship("UrlStatsModel", backref="url", uselist=False)

    def to_pydantic(self) -> 'UrlModelPydantic':
        return UrlModelPydantic(
            id=self.id,
            url=self.url,
            stats=self.stats.to_pydantic() if self.stats else UrlStats()
        )

class UrlModelPydantic(BaseModel):
    id: int
    url: str
    stats: UrlStats

    class Config:
        orm_mode = True

def create_database_session():
    try:
        engine = create_engine('sqlite:///database.db')
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        return Session()
    except Exception as e:
        logging.error(f"Error creating database session: {e}")
        raise

def get_url(session, url_id):
    try:
        return session.query(UrlModel).get(url_id)
    except Exception as e:
        logging.error(f"Error getting url: {e}")
        raise

def create_url(session, url):
    try:
        new_url = UrlModel(url=url)
        session.add(new_url)
        session.commit()
        return new_url
    except Exception as e:
        logging.error(f"Error creating url: {e}")
        session.rollback()
        raise

def update_url(session, url_id, url):
    try:
        url_to_update = session.query(UrlModel).get(url_id)
        if url_to_update:
            url_to_update.url = url
            session.commit()
        else:
            logging.error(f"Url with id {url_id} not found")
            raise ValueError(f"Url with id {url_id} not found")
    except Exception as e:
        logging.error(f"Error updating url: {e}")
        session.rollback()
        raise

def delete_url(session, url_id):
    try:
        url_to_delete = session.query(UrlModel).get(url_id)
        if url_to_delete:
            session.delete(url_to_delete)
            session.commit()
        else:
            logging.error(f"Url with id {url_id} not found")
            raise ValueError(f"Url with id {url_id} not found")
    except Exception as e:
        logging.error(f"Error deleting url: {e}")
        session.rollback()
        raise

def get_url_stats(session, url_id):
    try:
        url = session.query(UrlModel).get(url_id)
        if url and url.stats:
            return url.stats.to_pydantic()
        else:
            logging.error(f"Url with id {url_id} not found or has no stats")
            raise ValueError(f"Url with id {url_id} not found or has no stats")
    except Exception as e:
        logging.error(f"Error getting url stats: {e}")
        raise

def create_url_stats(session, url_id, stats):
    try:
        url = session.query(UrlModel).get(url_id)
        if url:
            new_stats = UrlStatsModel.from_pydantic(stats)
            url.stats = new_stats
            session.commit()
        else:
            logging.error(f"Url with id {url_id} not found")
            raise ValueError(f"Url with id {url_id} not found")
    except Exception as e:
        logging.error(f"Error creating url stats: {e}")
        session.rollback()
        raise

def update_url_stats(session, url_id, stats):
    try:
        url = session.query(UrlModel).get(url_id)
        if url and url.stats:
            url.stats.clicks = stats.clicks
            url.stats.impressions = stats.impressions
            url.stats.last_click = stats.last_click
            url.stats.last_impression = stats.last_impression
            session.commit()
        else:
            logging.error(f"Url with id {url_id} not found or has no stats")
            raise ValueError(f"Url with id {url_id} not found or has no stats")
    except Exception as e:
        logging.error(f"Error updating url stats: {e}")
        session.rollback()
        raise

def delete_url_stats(session, url_id):
    try:
        url = session.query(UrlModel).get(url_id)
        if url and url.stats:
            session.delete(url.stats)
            session.commit()
        else:
            logging.error(f"Url with id {url_id} not found or has no stats")
            raise ValueError(f"Url with id {url_id} not found or has no stats")
    except Exception as e:
        logging.error(f"Error deleting url stats: {e}")
        session.rollback()
        raise