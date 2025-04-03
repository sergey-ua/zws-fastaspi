package zws.schemas

from pydantic import BaseModel
from typing import Optional

class VisitShortUrlQueryDto(BaseModel):
    visit: Optional[bool] = True

class LongUrlDto(BaseModel):
    url: str