```python
from fastapi import APIRouter, HTTPException, Depends
from fastapi import status
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel, validator
from typing import Optional
from zws.database import Base, engine, SessionLocal
from zws.services.url_stats_service import UrlStatsService
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

class UrlStatsSchema(BaseModel):
    short_url: str
    clicks: int
    created_at: str

    class Config:
        orm_mode = True

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_url_stats_service():
    return UrlStatsService()

@router.get("/{short_url}/stats", response_model=UrlStatsSchema)
def get_url_stats(short_url: str, db: SessionLocal = Depends(get_db), url_stats_service: UrlStatsService = Depends(get_url_stats_service)):
    try:
        if not short_url:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Short URL is required")
        url_stats = url_stats_service.get_url_stats(db, short_url)
        if url_stats is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="URL statistics not found")
        return url_stats
    except Exception as e:
        logger.error(f"Error getting URL stats: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")

class UrlStatsRequest(BaseModel):
    short_url: str

    @validator('short_url')
    def short_url_must_be_valid(cls, v):
        if not v:
            raise ValueError('Short URL is required')
        return v
```