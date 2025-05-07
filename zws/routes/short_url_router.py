package zws.routes

import fastapi
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from short_url_service import ShortUrlService
import uvicorn
import contextlib
from zws.dependencies import Dependencies
from zws.routes.api import ApiRoutes

app = FastAPI()

short_url_service = ShortUrlService()
dependencies = Dependencies()
api_routes = ApiRoutes()

@app.get("/{short_url}")
async def redirect_to_long_url(short_url: str):
    try:
        if not short_url_service or not dependencies or not api_routes:
            raise HTTPException(status_code=500, detail="Services not initialized")
        if short_url_service.is_blocked(short_url):
            raise HTTPException(status_code=403, detail="Short URL is blocked")
        long_url = short_url_service.get_long_url(short_url)
        if not long_url:
            raise HTTPException(status_code=404, detail="Long URL not found")
        return RedirectResponse(url=long_url, status_code=302)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)