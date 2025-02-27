from urllib.parse import urlparse

from fastapi import APIRouter, Depends, Query

from zws.dependencies import get_blocked_hostnames_service
from zws.schemas.blocked_info_schema import BlockedInfoResponse
from zws.services.blocked_hostnames_service import BlockedHostnamesService

blocked_router = APIRouter()

@blocked_router.get("/check_url", response_model=BlockedInfoResponse)
def check_url(url_to_check: str = Query(..., alias="url_to_check"),
              blocked_hostnames_service: BlockedHostnamesService = Depends(get_blocked_hostnames_service)) -> BlockedInfoResponse:
    hostname = urlparse(url_to_check).hostname
    if not hostname:
        return BlockedInfoResponse(hostname="", is_blocked=False)
    is_blocked = blocked_hostnames_service.is_url_blocked(url_to_check)
    return BlockedInfoResponse(hostname=hostname, is_blocked=is_blocked)