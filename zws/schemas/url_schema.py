package zws.schemas

from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class UrlSchema(BaseModel):
    original_url: str
    shortened_url: str
    timestamp: datetime
    error: Optional[str] = None

    class Config:
        orm_mode = True