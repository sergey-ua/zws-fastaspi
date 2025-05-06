package zws.schemas

from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class UrlStatsSchema(BaseModel):
    id: int
    short_url: str
    visits: int
    created_at: datetime

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
        json_encoders = {datetime: lambda dt: dt.isoformat()}

class UrlStats(Base):
    __tablename__ = 'url_stats'
    id = Column(Integer, primary_key=True)
    short_url = Column(String)
    visits = Column(Integer)
    created_at = Column(DateTime)