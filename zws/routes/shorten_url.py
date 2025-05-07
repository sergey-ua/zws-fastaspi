from fastapi import APIRouter, HTTPException, Depends, FastAPI
from pydantic import BaseModel
from zws.services.blocked_hostnames_service import BlockedHostnamesService
from zws.services.url_mapping_service import UrlMappingService

router = APIRouter()

class LongUrlDto(BaseModel):
    url: str

class ShortenedUrlDto(BaseModel):
    short: str
    url: str

@router.post("/", response_model=ShortenedUrlDto)
async def shorten_url(
    request: LongUrlDto,
    blocked_hostnames_service: BlockedHostnamesService = Depends(),
    url_mapping_service: UrlMappingService = Depends(),
):
    try:
        if blocked_hostnames_service.is_url_blocked(request.url):
            raise HTTPException(status_code=422, detail="That URL hostname is blocked")
        
        short_identifier = url_mapping_service.generate_short_url(request.url)
        if not short_identifier:
            raise HTTPException(status_code=500, detail="Unable to generate a unique short ID within the max number of attempts")
        
        base_url = url_mapping_service.get_base_url()
        if not base_url:
            raise HTTPException(status_code=500, detail="Base URL configuration is missing")
        
        shortened_url = f"{base_url}/{short_identifier}"
        return ShortenedUrlDto(short=short_identifier, url=shortened_url)
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

app = FastAPI()
app.include_router(router, prefix="/shorten")