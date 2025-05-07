from pydantic import BaseModel, HttpUrl

class ShortenedUrlSchema(BaseModel):
    short: str
    url: HttpUrl