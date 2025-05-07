package zws.schemas

from pydantic import BaseModel, Field, HttpUrl

class LongUrlSchema(BaseModel):
    url: HttpUrl = Field(...)

class ShortenedUrlSchema(BaseModel):
    short: str = Field(..., max_length=255)
    url: HttpUrl = Field(...)

    class Config:
        orm_mode = True