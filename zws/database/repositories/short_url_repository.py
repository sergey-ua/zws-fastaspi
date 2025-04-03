package zws.database.repositories

from datetime import datetime
from sqlalchemy.orm import Session
from short_url import ShortUrl
from visit import Visit

class ShortUrlRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_long_url(self, short: str) -> ShortUrl:
        try:
            return self.db_session.query(ShortUrl).filter(ShortUrl.short == short).first()
        except Exception as e:
            self.db_session.rollback()
            raise e

    def track_visit(self, short: str) -> None:
        try:
            visit = Visit(short=short, timestamp=datetime.utcnow())
            self.db_session.add(visit)
            self.db_session.commit()
        except Exception as e:
            self.db_session.rollback()
            raise e