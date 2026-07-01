from fastapi import APIRouter

from zws.schemas.hello_schema import HelloResponse

hello_router = APIRouter(prefix="/hello", tags=["hello"])


@hello_router.get("/")
def hello() -> HelloResponse:
    return HelloResponse(msg="Hello World")
