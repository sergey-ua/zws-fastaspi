package zws.routes

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from fastapi import status
from zws.services import blocked_hostnames_service
import logging

logger = logging.getLogger(__name__)

class BlockedHostnamesRoute:
    def __init__(self):
        self.blocked_hostnames_service = blocked_hostnames_service.BlockedHostnamesService()
        self.router = APIRouter()

    def get_blocked_hostnames(self):
        try:
            blocked_hostnames = self.blocked_hostnames_service.get_blocked_hostnames()
            if blocked_hostnames is None:
                logger.error("Failed to retrieve blocked hostnames")
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to retrieve blocked hostnames")
            return blocked_hostnames
        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An error occurred")

    def route(self):
        @self.router.get("/blocked-hostnames")
        async def read_blocked_hostnames():
            return JSONResponse(content=self.get_blocked_hostnames(), media_type="application/json")
        return self.router

blocked_hostnames_route = BlockedHostnamesRoute()
router = blocked_hostnames_route.route()