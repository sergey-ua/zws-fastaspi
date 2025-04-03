package zws.schemas

from pydantic import BaseModel, HttpUrl

class ShortenedUrlDto(BaseModel):
    short: str
    url: HttpUrl