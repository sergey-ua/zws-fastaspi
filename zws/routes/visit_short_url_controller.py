```python
package zws.routes

from fastapi import APIRouter, HTTPException, Response
from fastapi import status
from pydantic import BaseModel
from zws.services import UrlsService
from zws.database.models import Short, LongUrl
from zws.schemas import LongUrlDto, VisitShortUrlQueryDto
from typing import Optional

router = APIRouter()

class NotFoundException(Exception):
    pass

class GoneException(Exception):
    pass

@router.get("/visit_short_url")
async def visit_short_url_controller(raw_short: str, query: Optional[VisitShortUrlQueryDto] = None):
    try:
        parsed_short = Short.parse(raw_short)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    original_url = UrlsService.retrieve_url(parsed_short)
    if original_url is None:
        raise HTTPException(status_code=404, detail='Shortened URL could not be found')
    if original_url.blocked:
        raise HTTPException(status_code=410, detail='URL is blocked and cannot be accessed')

    if query is None or query.visit is False:
        return LongUrlDto(original_url=original_url.url)

    UrlsService.track_url_visit(parsed_short)
    return Response(status_code=308, headers={"Location": original_url.url})
```