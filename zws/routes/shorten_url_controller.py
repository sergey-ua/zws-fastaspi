```python
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from zws.services import BlockedHostnamesService
from zws.database.repositories import UrlRepository
from zws.schemas import LongUrlDto, ShortenedUrlDto
from zws.database.models import Url, Base
from datetime import datetime
import base64
import uuid
from urllib.parse import urlparse
from pydantic import ValidationError
from typing import Optional
from sqlalchemy import Column, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

class URL:
    def __init__(self, url):
        self.url = url
        self.hostname = urlparse(url).hostname

class UnprocessableEntityException(Exception):
    pass

def generate_short_id():
    return uuid.uuid4().int

def to_base64(short_id):
    return base64.b64encode(short_id.to_bytes((short_id.bit_length() + 7) // 8, 'big')).decode('utf-8')

def is_url_blocked(url):
    return BlockedHostnamesService.is_blocked(url.hostname)

router = APIRouter()

@router.post("/shorten_url")
async def shorten_url(long_url_dto: LongUrlDto, db_session: Session):
    try:
        long_url_dto = LongUrlDto(url=long_url_dto.url)
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=e)

    url = URL(long_url_dto.url)
    if is_url_blocked(url):
        raise HTTPException(status_code=422, detail='That URL hostname is blocked')
    
    short_id = generate_short_id()
    short_base64 = to_base64(short_id)
    
    try:
        new_url = Url(url=long_url_dto.url, short_base64=short_base64, created_at=datetime.now(), blocked=False)
        db_session.add(new_url)
        db_session.commit()
    except IntegrityError as e:
        if e.code == '23505':
            pass
        else:
            raise HTTPException(status_code=500, detail=str(e))
    
    shortened_url_dto = ShortenedUrlDto(short=short_base64, url=url.url)
    return JSONResponse(content=shortened_url_dto.dict(), media_type="application/json")
```