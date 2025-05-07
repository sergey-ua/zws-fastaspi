from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from zws.services.short_url_service import ShortUrlService
from zws.services.visit_service import VisitService
from pydantic import BaseModel

router = APIRouter()

class OriginalUrlResponse(BaseModel):
    original_url: str

@router.get('/visit/{short}', response_model=OriginalUrlResponse)
def visit_short_url(
    short: str,
    visit: bool = True,
    db_session: Session = Depends(),
    short_url_service: ShortUrlService = Depends(),
    visit_service: VisitService = Depends()
):
    if not short or not short.isalnum():
        raise HTTPException(status_code=400, detail="Invalid shortened URL identifier")

    url_data = short_url_service.retrieve_url(short, db_session)
    if not url_data:
        raise HTTPException(status_code=404, detail="That shortened URL couldn't be found")
    if url_data.blocked:
        raise HTTPException(status_code=410, detail="That URL is blocked and can't be accessed")

    if not visit:
        return OriginalUrlResponse(original_url=url_data.original_url)

    visit_service.track_url_visit(short, db_session)
    return RedirectResponse(url=url_data.original_url, status_code=308)