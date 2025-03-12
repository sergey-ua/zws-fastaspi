package zws.database.models

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, DateTime, ForeignKey
from datetime import datetime

Base = declarative_base()

class Visit(Base):
    __tablename__ = 'visits'
    id = Column(Integer, primary_key=True)
    shortened_url_id = Column(Integer, ForeignKey('shorts.id'))
    timestamp = Column(DateTime, default=datetime.now)