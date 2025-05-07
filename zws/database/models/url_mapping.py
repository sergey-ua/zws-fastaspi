from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Boolean, DateTime, Integer, func

Base = declarative_base()

class UrlMapping(Base):
    __tablename__ = 'url_mappings'

    id = Column(Integer, primary_key=True, autoincrement=True)
    long_url = Column(String, unique=True, nullable=False)
    short_identifier = Column(String, unique=True, nullable=False, index=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    is_blocked = Column(Boolean, default=False, nullable=False)

    def __repr__(self):
        return f"<UrlMapping(id={self.id}, long_url={self.long_url}, short_identifier={self.short_identifier}, created_at={self.created_at}, is_blocked={self.is_blocked})>"