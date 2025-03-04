```python
package zws.database.repositories

from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from url_model import UrlModel
import logging

Base = declarative_base()

class Url(Base):
    __tablename__ = 'urls'
    id = Column(Integer, primary_key=True)
    original_url = Column(String)
    shortened_url = Column(String)

class UrlRepository:
    def __init__(self, db_url):
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def store_url(self, url_model):
        try:
            url = Url(original_url=url_model.original_url, shortened_url=url_model.shortened_url)
            self.session.add(url)
            self.session.commit()
        except Exception as e:
            logging.error(f"Error storing URL: {e}")
            self.session.rollback()
            raise

    def get_url(self, shortened_url):
        try:
            return self.session.query(Url).filter_by(shortened_url=shortened_url).first()
        except Exception as e:
            logging.error(f"Error retrieving URL: {e}")
            raise
```