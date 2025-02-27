from fastapi import APIRouter

from zws.routes.blocked_info import blocked_router

api_router = APIRouter()

api_router.include_router(blocked_router,
                          prefix="/blocked",
                          tags=["blocked"])