package zws.schemas

from pydantic import BaseModel, Field

class BlockedInfoResponse(BaseModel):
    hostname: str = Field(..., description="Hostname")
    blocked: bool = Field(..., description="Blocked status")