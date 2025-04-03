package zws.database.models

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime

Base = declarative_base()

class ShortUrl(Base):
    __tablename__ = 'short_urls'
    id = Column(Integer, primary_key=True)
    short = Column(String, unique=True, nullable=False)
    long_url = Column(String, nullable=False)
    blocked = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<ShortUrl(short={self.short}, long_url={self.long_url}, blocked={self.blocked})>'