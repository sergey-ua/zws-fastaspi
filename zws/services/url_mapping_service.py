from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from datetime import datetime
import uuid
from zws.database.models.url_mapping import UrlMapping

class UrlMappingService:
    MAX_SHORT_ID_GENERATION_ATTEMPTS = 5

    def __init__(self, db_session: Session):
        self.db_session = db_session

    def generate_short_url(self, url: str) -> str:
        attempts = 0
        while attempts < self.MAX_SHORT_ID_GENERATION_ATTEMPTS:
            short_id = uuid.uuid4().hex[:6]
            if self.is_short_id_unique(short_id):
                try:
                    new_mapping = UrlMapping(
                        url=url,
                        short_id=short_id,
                        created_at=datetime.utcnow()
                    )
                    self.db_session.add(new_mapping)
                    self.db_session.commit()
                    return short_id
                except IntegrityError:
                    self.db_session.rollback()
            attempts += 1
        raise Exception("Failed to generate a unique short URL after multiple attempts.")

    def is_short_id_unique(self, short_id: str) -> bool:
        return not self.db_session.query(UrlMapping).filter_by(short_id=short_id).first()