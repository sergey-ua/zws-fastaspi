package zws.services

from fastapi import FastAPI
from sqlalchemy.orm import Session
from zws.database.repositories import UrlsRepository
from zws.database.models import Short, LongUrl, Visit
from zws.exceptions import NotFoundException, GoneException

class UrlsService:
    def __init__(self, db_session: Session):
        self.db_session = db_session
        self.urls_repository = UrlsRepository(db_session)

    def retrieve_url(self, parsed_short: str):
        short_url = self.urls_repository.get_short_url(parsed_short)
        if short_url is None:
            self.handle_not_found_exception()
        if short_url.is_blocked:
            self.handle_gone_exception()
        return short_url.original_url

    def track_url_visit(self, parsed_short: str):
        short_url = self.urls_repository.get_short_url(parsed_short)
        if short_url is None:
            self.handle_not_found_exception()
        if short_url.is_blocked:
            self.handle_gone_exception()
        visit = Visit(short_url_id=short_url.id)
        self.urls_repository.add_visit(visit)

    def handle_not_found_exception(self):
        raise NotFoundException("Shortened URL could not be found")

    def handle_gone_exception(self):
        raise GoneException("URL is blocked and cannot be accessed")