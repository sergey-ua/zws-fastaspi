package zws.routes

from fastapi import APIRouter, Depends
from zws.schemas.long_url_dto import LongUrlDto
from zws.schemas.shortened_url_dto import ShortenedUrlDto
from zws.services.urls_service import UrlsService

router = APIRouter()

async def get_urls_service() -> UrlsService:
    return UrlsService()

@router.post('/shorten-url', response_model=ShortenedUrlDto)
async def shorten_url(long_url_dto: LongUrlDto, urls_service: UrlsService = Depends(get_urls_service)):
    return await urls_service.shorten_url(long_url_dto.url)