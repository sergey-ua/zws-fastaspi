package zws.database.models

import sqlalchemy as db
from sqlalchemy import Column, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
from contextlib import contextmanager
from zws.database.models import Base

class ShortURLModel(Base):
    __tablename__ = 'short_url'

    short_url = Column(String, primary_key=True)
    long_url = Column(String, nullable=False)
    is_blocked = Column(Boolean, default=False)

    def __repr__(self):
        return f'ShortURLModel(short_url={self.short_url}, long_url={self.long_url}, is_blocked={self.is_blocked})'

class ShortURLSchema(BaseModel):
    short_url: str
    long_url: str
    is_blocked: bool

    class Config:
        orm_mode = True

@contextmanager
def session_scope():
    session = Base.session
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()