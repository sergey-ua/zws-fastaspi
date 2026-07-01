from fastapi import APIRouter

from zws.routes.blocked_info import blocked_router
from zws.routes.hello import hello_router

api_router = APIRouter()

api_router.include_router(blocked_router,
                          prefix="/blocked",
                          tags=["blocked"])

api_router.include_router(hello_router)