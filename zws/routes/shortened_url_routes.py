package zws.routes

from fastapi import APIRouter, HTTPException, Depends, Query
from pydantic import BaseModel, Field
from zws.services.shortened_url_service import ShortenedUrlService
from fastapi.responses import RedirectResponse

router = APIRouter()

class ShortenUrlRequest(BaseModel):
    url: str = Field(..., description="The URL to be shortened")

class ShortenUrlResponse(BaseModel):
    short_url: str = Field(..., description="The shortened URL")
    metadata: dict = Field(..., description="Metadata associated with the shortened URL")

class ExpandUrlResponse(BaseModel):
    original_url: str = Field(..., description="The original URL associated with the short ID")

class VisitUrlResponse(BaseModel):
    long_url: str = Field(..., description="The original URL associated with the short base64")

@router.post(
    "/shorten",
    response_model=ShortenUrlResponse,
    summary="Shorten a URL",
    description="Generate a shortened URL for the provided original URL",
    responses={
        200: {"description": "Shortened URL generated successfully"},
        400: {"description": "Invalid input or processing error"}
    }
)
async def shorten_url(request: ShortenUrlRequest, service: ShortenedUrlService = Depends()):
    try:
        result = service.shorten_url(request.url)
        return ShortenUrlResponse(short_url=result["short_url"], metadata=result["metadata"])
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get(
    "/expand/{short_id}",
    response_model=ExpandUrlResponse,
    summary="Expand a shortened URL",
    description="Retrieve the original URL associated with the given short ID",
    responses={
        200: {"description": "Original URL retrieved successfully"},
        404: {"description": "Short ID not found"},
        400: {"description": "Invalid input or processing error"}
    }
)
async def expand_url(short_id: str, service: ShortenedUrlService = Depends()):
    try:
        original_url = service.get_original_url(short_id)
        return ExpandUrlResponse(original_url=original_url)
    except KeyError:
        raise HTTPException(status_code=404, detail="Short ID not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get(
    "/visit/{short_base64}",
    summary="Visit a shortened URL",
    description="Redirect to the original URL or return the URL details based on the visit parameter",
    responses={
        200: {"description": "URL details retrieved successfully"},
        302: {"description": "Redirected to the original URL"},
        404: {"description": "URL not found"},
        410: {"description": "URL is blocked"},
        400: {"description": "Invalid input or processing error"}
    }
)
async def visit_url(
    short_base64: str,
    visit: bool = Query(
        default=True,
        description="Whether to visit the URL (redirect) or return its details"
    ),
    service: ShortenedUrlService = Depends()
):
    try:
        url_record = service.retrieve_url(short_base64)
        if not url_record:
            raise HTTPException(status_code=404, detail="URL not found")
        if url_record.get("blocked"):
            raise HTTPException(status_code=410, detail="URL is blocked")
        if visit:
            service.track_url_visit(short_base64)
            return RedirectResponse(url=url_record["long_url"])
        return VisitUrlResponse(long_url=url_record["long_url"])
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))