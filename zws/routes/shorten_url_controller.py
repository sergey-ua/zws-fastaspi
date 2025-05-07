package zws.routes

from fastapi import APIRouter, HTTPException, status
from zws.services.urls_service import UrlsService, BlockedUrlException, ShortIdGenerationException
from zws.schemas.long_url_schema import LongUrlSchema
from zws.schemas.shortened_url_schema import ShortenedUrlSchema

router = APIRouter()

@router.post("/shorten-url", response_model=ShortenedUrlSchema, status_code=status.HTTP_201_CREATED)
async def shorten_url(request: LongUrlSchema):
    try:
        shortened_url_data = UrlsService.shorten_url(request.long_url)
        return ShortenedUrlSchema(**shortened_url_data)
    except BlockedUrlException:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="That URL hostname is blocked"
        )
    except ShortIdGenerationException:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to generate a unique short ID"
        )