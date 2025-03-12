package database.models

from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Url(Base):
    __tablename__ = 'urls'
    id = Column(Integer, primary_key=True)
    url = Column(String, nullable=False)
    short_base64 = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    blocked = Column(Boolean, nullable=False, default=False)