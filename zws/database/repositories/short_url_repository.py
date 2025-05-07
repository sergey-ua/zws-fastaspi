```python
package zws.database.repositories

from zws.database.models import url_model
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sqlalchemy as db
from typing import Optional

class ShortUrlRepository:
    def __init__(self, db_url: str):
        self.engine = create_engine(db_url)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def get_short_url(self, short_url_id: int) -> Optional[url_model.ShortUrl]:
        try:
            if not isinstance(short_url_id, int) or short_url_id <= 0:
                raise ValueError("Short URL ID must be a positive integer")
            short_url = self.session.query(url_model.ShortUrl).filter_by(id=short_url_id).first()
            if not short_url:
                raise ValueError("Short URL not found")
            return short_url
        except db.exc.SQLAlchemyError as e:
            self.session.rollback()
            raise e

    def get_short_url_by_code(self, code: str) -> Optional[url_model.ShortUrl]:
        try:
            if not isinstance(code, str) or not code.strip():
                raise ValueError("Code must be a non-empty string")
            short_url = self.session.query(url_model.ShortUrl).filter_by(code=code).first()
            if not short_url:
                raise ValueError("Short URL not found")
            return short_url
        except db.exc.SQLAlchemyError as e:
            self.session.rollback()
            raise e

    def create_short_url(self, original_url: str, code: str) -> url_model.ShortUrl:
        try:
            if not isinstance(original_url, str) or not original_url.strip():
                raise ValueError("Original URL must be a non-empty string")
            if not isinstance(code, str) or not code.strip():
                raise ValueError("Code must be a non-empty string")
            short_url = url_model.ShortUrl(original_url=original_url, code=code)
            self.session.add(short_url)
            self.session.commit()
            return short_url
        except db.exc.SQLAlchemyError as e:
            self.session.rollback()
            raise e

    def update_short_url(self, short_url_id: int, original_url: Optional[str] = None, code: Optional[str] = None) -> url_model.ShortUrl:
        try:
            if not isinstance(short_url_id, int) or short_url_id <= 0:
                raise ValueError("Short URL ID must be a positive integer")
            short_url = self.session.query(url_model.ShortUrl).filter_by(id=short_url_id).first()
            if not short_url:
                raise ValueError("Short URL not found")
            if original_url:
                short_url.original_url = original_url
            if code:
                short_url.code = code
            self.session.commit()
            return short_url
        except db.exc.SQLAlchemyError as e:
            self.session.rollback()
            raise e

    def delete_short_url(self, short_url_id: int) -> url_model.ShortUrl:
        try:
            if not isinstance(short_url_id, int) or short_url_id <= 0:
                raise ValueError("Short URL ID must be a positive integer")
            short_url = self.session.query(url_model.ShortUrl).filter_by(id=short_url_id).first()
            if not short_url:
                raise ValueError("Short URL not found")
            self.session.delete(short_url)
            self.session.commit()
            return short_url
        except db.exc.SQLAlchemyError as e:
            self.session.rollback()
            raise e
```