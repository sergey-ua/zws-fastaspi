package zws.schemas

from pydantic import BaseModel, HttpUrl, validator

class LongUrlDto(BaseModel):
    url: HttpUrl

    @validator('url')
    def validate_url(cls, v):
        if not v:
            raise ValueError('URL must not be empty')
        return v