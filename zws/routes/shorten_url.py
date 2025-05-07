package zws.routes

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, HttpUrl, ValidationError
from zws.services.shortened_url import ShortenedUrlService
from zws.schemas.shortened_url import ShortenedUrlSchema

router = APIRouter()

class LongUrlSchema(BaseModel):
    url: HttpUrl

@router.post("/shorten-url", response_model=ShortenedUrlSchema, status_code=201)
async def shorten_url(
    request_body: LongUrlSchema,
    service: ShortenedUrlService = Depends()
):
    try:
        validated_url = request_body.url
        shortened_url = service.shorten_url(validated_url)
        return ShortenedUrlSchema(**shortened_url)
    except ValidationError:
        raise HTTPException(status_code=422, detail="Invalid URL")
    except ValueError as e:
        if str(e) == "URL_BLOCKED":
            raise HTTPException(status_code=422, detail="That URL hostname is blocked")
        elif str(e) == "UNIQUE_ID_ERROR":
            raise HTTPException(status_code=500, detail="Unable to generate a unique short ID")
        else:
            raise HTTPException(status_code=500, detail="An unexpected error occurred")
    except Exception:
        raise HTTPException(status_code=500, detail="An unexpected error occurred")