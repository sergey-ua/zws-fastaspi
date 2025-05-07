from sqlalchemy.orm import Session
from zws.database.models.visit import Visit
from zws.database.models.short_url import ShortURL
from datetime import datetime
import base64


class VisitService:
    def track_url_visit(self, short: str, db_session: Session):
        try:
            encoded_id = base64.b64encode(short.encode()).decode()

            short_url_record = db_session.execute(
                "SELECT short_base64 FROM short_url WHERE short_base64 = :encoded_id LIMIT 1",
                {"encoded_id": encoded_id}
            ).fetchone()

            if not short_url_record:
                raise Exception("Shortened URL does not exist.")

            current_time = datetime.utcnow()
            db_session.execute(
                "INSERT INTO visit (timestamp, short_base64) VALUES (:current_time, :encoded_id)",
                {"current_time": current_time, "encoded_id": encoded_id}
            )
            db_session.commit()
        except Exception as e:
            db_session.rollback()
            raise e