package zws.database.models

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

Base = declarative_base()

class BlockedHostname(Base):
    __tablename__ = 'blocked_hostnames'

    id = Column(Integer, primary_key=True)
    hostname = Column(String, nullable=False, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<BlockedHostname(id={self.id}, hostname={self.hostname}, created_at={self.created_at})>'