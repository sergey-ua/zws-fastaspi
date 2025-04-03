package zws.routes

from fastapi import APIRouter, HTTPException, Depends
from .schemas.visit_short_url_schema import VisitShortUrlQueryDto, LongUrlDto
from .repositories.short_url_repository import ShortUrlRepository

router = APIRouter()

def get_short_url_repository():
    return ShortUrlRepository()

@router.get('/short-url/{short}', response_model=LongUrlDto)
async def visit_short_url(short: str, query: VisitShortUrlQueryDto = Depends(), short_url_repository: ShortUrlRepository = Depends(get_short_url_repository)):
    url_data = short_url_repository.get_long_url(short)
    if not url_data:
        raise HTTPException(status_code=404, detail="That shortened URL couldn't be found")
    if url_data.blocked:
        raise HTTPException(status_code=410, detail="That URL is blocked and can't be accessed")
    if query.visit:
        short_url_repository.track_visit(short)
    return LongUrlDto(url=url_data.long_url)