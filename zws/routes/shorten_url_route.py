package zws.routes

from fastapi import APIRouter, Depends, HTTPException
from zws.services.url_service import UrlService
from zws.schemas.shortened_url_schema import ShortenedUrlSchema

shorten_url_router = APIRouter()

@shorten_url_router.post("/shorten-url")
async def shorten_url(
    request: ShortenedUrlSchema,
    url_service: UrlService = Depends()
):
    try:
        result = url_service.shorten_url(request)
        return {"short_identifier": result.short_identifier, "original_url": result.original_url}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred")