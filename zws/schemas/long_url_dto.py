from pydantic import BaseModel, Field

class LongUrlDto(BaseModel):
    original_url: str = Field(..., description="The original URL")
    url: str = Field(..., description="The shortened URL")