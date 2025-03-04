```python
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, validator
from zws.services import url_service
from typing import Dict
import logging

app = APIRouter()

class UrlInfo(BaseModel):
    long_url: str

    @validator('long_url')
    def validate_long_url(cls, v):
        if not v:
            raise ValueError('Long URL is required')
        if not v.startswith('http'):
            raise ValueError('Long URL must start with http')
        return v

class ErrorResponse(BaseModel):
    error: str

class ShortUrlResponse(BaseModel):
    short_url: str

@app.post("/", response_model=ShortUrlResponse, responses={
    400: {"model": ErrorResponse},
    500: {"model": ErrorResponse}
})
async def create_short_url(url_info: UrlInfo):
    try:
        short_url = url_service.create_short_url(url_info.long_url)
        if not short_url:
            raise ValueError('Failed to create short URL')
        return ShortUrlResponse(short_url=short_url)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logging.error("Internal Server Error: %s", e)
        raise HTTPException(status_code=500, detail="Internal Server Error")
```