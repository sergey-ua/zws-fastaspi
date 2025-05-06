package zws.database.models

from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from zws.database import Base

class ShortenedUrl(Base):
    __tablename__ = 'shortened_urls'

    id = Column(Integer, primary_key=True, autoincrement=True)
    original_url = Column(String, nullable=False)
    short_id = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    is_blocked = Column(Boolean, default=False, nullable=False)