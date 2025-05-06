package zws.schemas

from pydantic import BaseModel, Field, validator
from datetime import datetime
from pydantic.networks import AnyHttpUrl

class ShortenedUrlSchema(BaseModel):
    original_url: AnyHttpUrl
    short_identifier: str
    created_at: datetime
    blocked: bool

    @validator("short_identifier")
    def validate_short_identifier(cls, value):
        if not value.isalnum():
            raise ValueError("short_identifier must be alphanumeric")
        return value

    class Config:
        orm_mode = True