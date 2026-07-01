from pydantic import BaseModel


class HelloResponse(BaseModel):
    msg: str
