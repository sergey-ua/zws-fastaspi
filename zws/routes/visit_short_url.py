package zws.routes

from fastapi import APIRouter, Query, Response, HTTPException
from pydantic import BaseModel
from zws.services.shortened_url_service import ShortenedUrlService

router = APIRouter()

@router.get('/{short}')
async def visit_short_url(short: str, visit: bool = Query(default=True), response: Response):
    if not ShortenedUrlService.validate_short(short):
        raise HTTPException(status_code=400, detail='Invalid shortened URL identifier')
    
    url_data = ShortenedUrlService.retrieve_url(short)
    if url_data is None:
        raise HTTPException(status_code=404, detail='Shortened URL not found')
    
    if url_data['blocked']:
        raise HTTPException(status_code=410, detail='URL is blocked')
    
    long_url = url_data['url']
    
    if visit:
        ShortenedUrlService.track_url_visit(short)
        response.headers['Location'] = long_url
        return Response(status_code=308)
    
    return {"url": long_url}

def include_router(app):
    app.include_router(router)