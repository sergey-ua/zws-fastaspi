package zws.database.models

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, DateTime
from datetime import datetime

Base = declarative_base()

class ShortenedUrlModel(Base):
    __tablename__ = 'shortened_urls'

    id = Column(Integer, primary_key=True, autoincrement=True)
    short = Column(String, unique=True, nullable=False)
    url = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)