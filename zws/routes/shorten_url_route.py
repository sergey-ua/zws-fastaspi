```python
from fastapi import APIRouter, FastAPI, Depends, HTTPException
from pydantic import ValidationError
from zws.services.blocked_hostnames_service import BlockedHostnamesService
from zws.schemas.long_url_dto import LongUrlDto
from zws.schemas.shortened_url_dto import ShortenedUrlDto
import hashlib
import uuid
from typing import Dict

package = __package__

class ShortenUrlRoute:
    def __init__(self, blocked_hostnames_service: BlockedHostnamesService):
        self.router = APIRouter()
        self.blocked_hostnames_service = blocked_hostnames_service
        self.url_map: Dict[str, str] = {}

    def shorten_url(self, long_url_dto: LongUrlDto):
        try:
            if not isinstance(long_url_dto, LongUrlDto):
                raise HTTPException(status_code=400, detail="Invalid request body")
            if self.blocked_hostnames_service.is_blocked(long_url_dto.url):
                raise HTTPException(status_code=400, detail="Hostname is blocked")
            shortened_url = self.generate_shortened_url(long_url_dto.url)
            while shortened_url in self.url_map:
                shortened_url = self.generate_shortened_url(long_url_dto.url)
            self.url_map[shortened_url] = long_url_dto.url
            return ShortenedUrlDto(shortened_url=shortened_url)
        except ValidationError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def generate_shortened_url(self, url: str):
        return str(uuid.uuid4())[:6]

    def get_router(self):
        self.router.post("/shorten-url", response_model=ShortenedUrlDto)(self.shorten_url)
        return self.router

def main():
    app = FastAPI()
    blocked_hostnames_service = BlockedHostnamesService()
    shorten_url_route = ShortenUrlRoute(blocked_hostnames_service)
    app.include_router(shorten_url_route.get_router())
    return app

if __name__ == "__main__":
    import uvicorn
    app = main()
    uvicorn.run(app, host="0.0.0.0", port=8000)
```