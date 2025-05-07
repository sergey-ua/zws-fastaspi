package zws.schemas

from pydantic import BaseModel, HttpUrl

class LongUrlSchema(BaseModel):
    url: HttpUrl