package zws.routes

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from zws.services import UrlsService
from zws.schemas.shortened_url_dto import ShortenedUrlDto
from zws.exceptions import UnprocessableEntityException, InternalServerErrorException
from zws.utils import is_valid_url

router = APIRouter()

class ShortenUrlRequest(BaseModel):
    url: str

@router.post("/shorten-url", response_model=ShortenedUrlDto)
async def shorten_url(request: ShortenUrlRequest):
    long_url = request.url
    if not long_url:
        raise HTTPException(status_code=400, detail='URL is required')
    if not is_valid_url(long_url):
        raise HTTPException(status_code=400, detail='Invalid URL format')

    try:
        urls_service = UrlsService()
        result = await urls_service.shorten_url(long_url)
        return JSONResponse(status_code=200, content=result)
    except UnprocessableEntityException as e:
        raise HTTPException(status_code=422, detail=str(e))
    except InternalServerErrorException as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail='An unexpected error occurred')