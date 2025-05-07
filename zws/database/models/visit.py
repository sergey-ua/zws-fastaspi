from sqlalchemy import Column, Integer, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from /zws/database/models/short_url import ShortUrl

Base = declarative_base()

class Visit(Base):
    __tablename__ = 'visits'

    id = Column(Integer, primary_key=True, autoincrement=True)
    short_url_id = Column(Integer, ForeignKey('short_url.id'), nullable=False)
    timestamp = Column(DateTime(timezone=True), default=func.now(), nullable=False)

    short_url = relationship('ShortUrl', back_populates='visits')

    def to_dict(self):
        return {
            'id': self.id,
            'short_url_id': self.short_url_id,
            'timestamp': self.timestamp.isoformat()
        }