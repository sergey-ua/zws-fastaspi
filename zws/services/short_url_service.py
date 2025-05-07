from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from zws.database.models.short_url import ShortUrl
import base64
import aioredis

class ShortUrlService:
    def __init__(self, redis_client=None):
        self.redis_client = redis_client or aioredis.from_url("redis://localhost")

    async def retrieve_url(self, short: str, db_session: Session):
        try:
            encoded_id = base64.b64encode(short.encode()).decode()
            result = db_session.query(ShortUrl.url, ShortUrl.blocked).filter(ShortUrl.short_base64 == encoded_id).limit(1).one_or_none()
            
            if not result:
                return None
            
            url, blocked = result
            if await self.is_url_blocked(url):
                if not blocked:
                    db_session.query(ShortUrl).filter(ShortUrl.short_base64 == encoded_id).update({"blocked": True})
                    db_session.commit()
                return {"long_url": None, "blocked": True}
            
            return {"long_url": url, "blocked": False}
        except SQLAlchemyError:
            db_session.rollback()
            raise

    async def is_url_blocked(self, url: str):
        try:
            hostname = url.split('/')[2]
            cached_blocked = await self.redis_client.get(hostname)
            if cached_blocked:
                return True
            
            blocked_patterns = ["malicious.com", "phishing.net"]
            if any(pattern in url for pattern in blocked_patterns):
                await self.redis_client.set(hostname, "1", ex=3600)
                return True
            
            return False
        except Exception:
            return True