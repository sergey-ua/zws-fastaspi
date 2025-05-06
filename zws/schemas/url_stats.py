from pydantic import BaseModel
from typing import List

class Referrer(BaseModel):
    url: str
    count: int

class UrlStats(BaseModel):
    url: str
    clicks: int
    visits: int
    referrers: List[Referrer]

    class Config:
        orm_mode = True