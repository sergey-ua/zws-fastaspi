```python
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from zws.services.shortened_url_service import ShortenedUrlService

router = APIRouter()

class LongUrlDto(BaseModel):
    url: str

class ShortenedUrlDto(BaseModel):
    short: str
    url: str

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ShortenedUrlDto)
async def shorten_url(request: LongUrlDto):
    try:
        shortened_url = ShortenedUrlService().shorten_url(request.url)
        return ShortenedUrlDto(short=shortened_url.short, url=shortened_url.url)
    except ValueError as e:
        if str(e) == "Invalid URL":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid URL provided")
        elif str(e) == "Blocked URL":
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="That URL hostname is blocked")
        elif str(e) == "Max Attempts Exceeded":
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unable to generate a unique short ID within the max number of attempts")
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected error occurred")
```