package zws.database.models

from sqlalchemy import Column, String, Boolean, Integer, DateTime, Index, event, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class UrlModel(Base):
    __tablename__ = 'urls'

    id = Column(Integer, primary_key=True, autoincrement=True)
    short_base64 = Column(String, unique=True, nullable=False, index=True)
    long_url = Column(String, nullable=False)
    blocked = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    __table_args__ = (
        UniqueConstraint('short_base64', name='uq_short_base64'),
    )

    @staticmethod
    def _update_timestamp(mapper, connection, target):
        target.updated_at = datetime.utcnow()

event.listen(UrlModel, 'before_update', UrlModel._update_timestamp)