from pydantic import BaseModel

class BlockedInfoResponse(BaseModel):
    hostname: str
    is_blocked: bool