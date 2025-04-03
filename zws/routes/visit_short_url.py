package zws.routes

from fastapi import APIRouter, Response, HTTPException
from zws.schemas.visit_short_url_schema import VisitShortUrlQueryDto, LongUrlDto
from zws.services import UrlsService
from zws.exceptions import BadRequestException, NotFoundException, GoneException
from zws.models import Short

router = APIRouter()
urls_service = UrlsService()

@router.get("/visit/{raw_short}")
def visit_short_url(raw_short: str, query: VisitShortUrlQueryDto, response: Response) -> LongUrlDto:
    try:
        short = Short.parse(raw_short)
    except Exception:
        raise BadRequestException('Invalid shortened URL format')

    url_data = urls_service.retrieve_url(short)
    if url_data is None:
        raise NotFoundException('That shortened URL couldn\'t be found')

    if url_data.blocked:
        raise GoneException('That URL is blocked and can\'t be accessed')

    if query.visit is not False:
        urls_service.track_url_visit(short)

    response.redirect(308, url_data.long_url)
    return LongUrlDto(url=url_data.long_url) if query.visit else None