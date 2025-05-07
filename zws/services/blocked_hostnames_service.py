package zws.services

import base64
from sqlalchemy.orm import Session
from zws.database.models.url_model import URLModel
from zws.database.models.visit_model import VisitModel
from datetime import datetime

class BlockedHostnamesService:
    @staticmethod
    def retrieve_url(short: str, session: Session) -> dict:
        encoded_id = BlockedHostnamesService.to_base64(short)
        url_record = session.query(URLModel).filter(URLModel.short_base64 == encoded_id).limit(1).one_or_none()
        
        if not url_record:
            return None
        
        if not url_record.blocked:
            url_record.blocked = True
            session.commit()
        
        return {"long_url": url_record.url, "blocked": url_record.blocked}

    @staticmethod
    def track_url_visit(short: str, session: Session) -> None:
        encoded_id = BlockedHostnamesService.to_base64(short)
        visit_record = VisitModel(timestamp=datetime.utcnow(), url_short_base64=encoded_id)
        session.add(visit_record)
        session.commit()

    @staticmethod
    def to_base64(input_str: str) -> str:
        return base64.b64encode(input_str.encode()).decode()