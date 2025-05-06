package zws.database.repositories

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy import func
from zws.database.models.shortened_url import ShortenedUrl
from zws.database.models.visit import Visit

class ShortenedUrlRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_short_base64(self, short_base64: str) -> ShortenedUrl | None:
        return self.session.query(ShortenedUrl).filter(ShortenedUrl.short_base64 == short_base64).one_or_none()

    def get_by_short_id(self, short_id: str) -> ShortenedUrl | None:
        return self.session.query(ShortenedUrl).filter(ShortenedUrl.short_id == short_id).one_or_none()

    def create_shortened_url(self, original_url: str, short_id: str, is_blocked: bool) -> ShortenedUrl:
        shortened_url = ShortenedUrl(original_url=original_url, short_id=short_id, is_blocked=is_blocked)
        self.session.add(shortened_url)
        self.session.commit()
        return shortened_url

    def insert_shortened_url(self, original_url: str, short_id: str, short_base64: str, is_blocked: bool) -> ShortenedUrl | None:
        try:
            shortened_url = ShortenedUrl(
                original_url=original_url,
                short_id=short_id,
                short_base64=short_base64,
                is_blocked=is_blocked
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

    def is_short_id_unique(self, short_id: str) -> bool:
        return not self.session.query(ShortenedUrl).filter(ShortenedUrl.short_id == short_id).first()

    def is_hostname_blocked(self, hostname: str) -> bool:
        return self.session.query(ShortenedUrl).filter(ShortenedUrl.original_url.contains(hostname)).first() is not None

    def update_blocked_status(self, short_base64: str, blocked: bool) -> ShortenedUrl | None:
        try:
            shortened_url = self.session.query(ShortenedUrl).filter(ShortenedUrl.short_base64 == short_base64).one_or_none()
            if shortened_url:
                shortened_url.is_blocked = blocked
                self.session.commit()
                return shortened_url
            return None
        except SQLAlchemyError:
            self.session.rollback()
            return None

    def track_visit(self, short_base64: str) -> bool:
        try:
            visit = Visit(short_base64=short_base64)
            self.session.add(visit)
            self.session.commit()
            return True
        except SQLAlchemyError:
            self.session.rollback()
            return False