package zws.routes

from fastapi import APIRouter, HTTPException, RedirectResponse
from zws.services import UrlsService
from zws.database.models import Url

router = APIRouter()

@router.get("/visitShortUrl/{short_url}")
async def visit_short_url_controller(short_url: str):
    urls_service = UrlsService()
    original_url = await urls_service.get_original_url(short_url)
    if original_url is None:
        raise HTTPException(status_code=404, detail="URL not found")
    await urls_service.track_visit(short_url)
    return RedirectResponse(url=original_url, status_code=302)