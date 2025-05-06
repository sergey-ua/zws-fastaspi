package zws.database.repositories

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from zws.database.models.shortened_url import ShortenedUrl
from zws.database.models.visit import Visit
from datetime import datetime

class ShortenedUrlRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_shortened_url(self, original_url: str, short_identifier: str, created_at: datetime, blocked: bool) -> ShortenedUrl | None:
        try:
            shortened_url = ShortenedUrl(
                original_url=original_url,
                short_identifier=short_identifier,
                created_at=created_at,
                blocked=blocked
            )
            self.session.add(shortened_url)
            self.session.commit()
            return shortened_url
        except IntegrityError:
            self.session.rollback()
            return None
        except SQLAlchemyError:
            self.session.rollback()
            return None

    def get_by_short_identifier(self, short_identifier: str) -> ShortenedUrl | None:
        try:
            return self.session.query(ShortenedUrl).filter(ShortenedUrl.short_identifier == short_identifier).one_or_none()
        except SQLAlchemyError:
            return None

    def is_url_blocked(self, original_url: str) -> bool:
        try:
            shortened_url = self.session.query(ShortenedUrl).filter(ShortenedUrl.original_url == original_url).one_or_none()
            return shortened_url.blocked if shortened_url else False
        except SQLAlchemyError:
            return False

    def track_visit(self, short_identifier: str) -> bool:
        try:
            visit = Visit(short_identifier=short_identifier, timestamp=datetime.utcnow())
            self.session.add(visit)
            self.session.commit()
            return True
        except SQLAlchemyError:
            self.session.rollback()
            return False