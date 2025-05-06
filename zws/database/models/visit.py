package zws.database.models

from sqlalchemy.orm.declarative_base import Base
from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from zws.database.models.shortened_url import ShortenedUrl

class Visit(Base):
    __tablename__ = 'visits'

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime(timezone=True), nullable=False)
    shortened_url_id = Column(Integer, ForeignKey('shortened_url.id'), nullable=False)

    shortened_url = relationship('ShortenedUrl', back_populates='visits')