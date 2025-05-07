```python
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import RedirectResponse, JSONResponse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from urllib.parse import urlparse
from zws.models import UrlModel
from zws.services import BlockedHostnamesService

package = __package__

router = APIRouter()
engine = create_engine("sqlite:///urls.db")
Session = sessionmaker(bind=engine)

@router.get("/short/{short_url}")
async def get_original_url(short_url: str):
    try:
        session = Session()
        url = session.query(UrlModel).filter(UrlModel.short_url == short_url).first()
        if not url:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="URL not found")
        original_url = url.original_url
        blocked_hostnames_service = BlockedHostnamesService()
        if blocked_hostnames_service.is_blocked(urlparse(original_url).hostname):
            return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={"error": "URL is blocked"})
        return RedirectResponse(url=original_url, status_code=status.HTTP_301_MOVED_PERMANENTLY)
    except HTTPException as e:
        raise e
    except Exception as e:
        session.close()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
    else:
        session.close()
```