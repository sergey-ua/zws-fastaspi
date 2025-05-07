package zws.routes

from fastapi import APIRouter, Depends
from zws.services.shortened_url_service import ShortenedUrlService
from zws.schemas.shortened_url import ShortenedUrlSchema

shortened_url_router = APIRouter()

@shortened_url_router.post("/shorten-url", response_model=ShortenedUrlSchema)
def shorten_url(
    request: ShortenedUrlSchema,
    service: ShortenedUrlService = Depends()
):
    return service.shorten_url(request)

@shortened_url_router.get("/shortened-url/{short}", response_model=ShortenedUrlSchema)
def get_shortened_url(
    short: str,
    service: ShortenedUrlService = Depends()
):
    return service.get_shortened_url(short)

@shortened_url_router.get("/shortened-urls", response_model=list[ShortenedUrlSchema])
def list_shortened_urls(
    service: ShortenedUrlService = Depends()
):
    return service.list_shortened_urls()