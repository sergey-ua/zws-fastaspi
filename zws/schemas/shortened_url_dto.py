package zws.schemas

from pydantic import BaseModel, Field

class ShortenedUrlDto(BaseModel):
    short: str = Field(..., description="Shortened URL")
    url: str = Field(..., description="Original URL")