```python
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, validator
from typing import Optional

from zws.services import BlockedHostnamesService
from zws.repositories import UrlRepository

app = FastAPI()

class UrlRequest(BaseModel):
    url: str

    @validator('url')
    def validate_url(cls, v):
        if not v:
            raise ValueError('URL is required')
        return v

class UrlResponse(BaseModel):
    url: str
    is_blocked: bool
    mapped_url: Optional[str]

blocked_hostnames_service = BlockedHostnamesService()
url_repository = UrlRepository()

@app.exception_handler(RequestValidationError)
async def validation_error_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(status_code=400, content={"detail": exc.errors()})

@app.post("/url", response_model=UrlResponse)
async def handle_url(url_request: UrlRequest):
    try:
        is_blocked = blocked_hostnames_service.is_blocked(url_request.url)
        if is_blocked:
            return UrlResponse(url=url_request.url, is_blocked=True)
        else:
            mapped_url = url_repository.store_url_mapping(url_request.url)
            return UrlResponse(url=url_request.url, is_blocked=False, mapped_url=mapped_url)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
```