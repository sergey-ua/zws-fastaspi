package zws.schemas

from pydantic import BaseModel

class VisitShortUrlQueryDto(BaseModel):
    visit: bool = True