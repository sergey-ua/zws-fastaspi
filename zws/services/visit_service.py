package zws.services

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
import base64
from zws.database.models.visit import Visit
from zws.database.models.shortened_url import ShortenedUrl

class VisitService:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def track_url_visit(self, short: str):
        try:
            encoded_id = base64.urlsafe_b64encode(short.encode()).decode()

            shortened_url = self.db_session.query(ShortenedUrl).filter_by(short_base64=encoded_id).first()
            if not shortened_url:
                raise ValueError("Shortened URL does not exist.")

            visit = Visit(timestamp=datetime.utcnow(), url_short_base64=encoded_id)
            self.db_session.add(visit)
            self.db_session.commit()
        except SQLAlchemyError as e:
            self.db_session.rollback()
            raise e
        except Exception as e:
            raise e