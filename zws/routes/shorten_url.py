package zws.routes.shorten_url

from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel, HttpUrl
from zws.services.blocked_hostnames_service import BlockedHostnamesService
from zws.services.shortened_url_service import ShortenedUrlService
from zws.schemas.shortened_url_schema import ShortenedUrlSchema
from zws.schemas.long_url_schema import LongUrlSchema

router = APIRouter()

class LongUrlSchema(BaseModel):
    url: HttpUrl

class ShortenedUrlSchema(BaseModel):
    short: str
    url: str

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ShortenedUrlSchema)
async def shorten_url(
    request: LongUrlSchema,
    blocked_hostnames_service: BlockedHostnamesService = Depends(),
    shortened_url_service: ShortenedUrlService = Depends()
):
    if blocked_hostnames_service.is_url_blocked(request.url):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="That URL hostname is blocked"
        )
    try:
        short_identifier = shortened_url_service.generate_short_url(request.url)
    except ValueError as e:
        if str(e) == "Max Attempts Exceeded":
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Unable to generate a unique short ID within the max number of attempts"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An unexpected error occurred"
            )
    base_url = shortened_url_service.get_base_url()
    shortened_url = f"{base_url}/{short_identifier}"
    return ShortenedUrlSchema(short=short_identifier, url=shortened_url)