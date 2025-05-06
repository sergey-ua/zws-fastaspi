package zws.database.models

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from database.base import Base
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UrlStatsModel(Base):
    __tablename__ = "url_stats"

    id = Column(Integer, primary_key=True, index=True)
    short_url = Column(String, unique=True, index=True)
    visits = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now())

class UrlStatsBase(BaseModel):
    short_url: str
    visits: int

class UrlStatsCreate(UrlStatsBase):
    pass

class UrlStatsUpdate(UrlStatsBase):
    short_url: Optional[str] = None
    visits: Optional[int] = None

class UrlStats(UrlStatsBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True