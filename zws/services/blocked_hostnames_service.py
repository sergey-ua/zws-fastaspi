```python
from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError, IntegrityError, DataError
from urllib.parse import urlparse
from typing import Optional

Base = declarative_base()

class BlockedHostname(Base):
    __tablename__ = 'blocked_hostnames'
    hostname = Column(String, primary_key=True)

class BlockedHostnamesService:
    def __init__(self, session_maker):
        self.session_maker = session_maker

    def is_url_blocked(self, url: str) -> bool:
        if not isinstance(url, str):
            raise TypeError("URL must be a string")
        try:
            session = self.session_maker()
            hostname = urlparse(url).hostname
            if not hostname:
                return False
            query = session.query(BlockedHostname).filter_by(hostname=hostname)
            result = query.first()
            session.close()
            return result is not None
        except (SQLAlchemyError, IntegrityError, DataError) as e:
            if 'session' in locals():
                session.close()
            raise e
        except Exception as e:
            if 'session' in locals():
                session.close()
            raise e

def check_if_url_blocked(url: str, blocked_hostnames_service: BlockedHostnamesService) -> bool:
    if not url:
        return False
    return blocked_hostnames_service.is_url_blocked(url)
```