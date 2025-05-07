from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ShortUrl(Base):
    __tablename__ = 'short_urls'

    id = Column(Integer, primary_key=True, autoincrement=True)
    short_base64 = Column(String, unique=True, nullable=False)
    long_url = Column(String, nullable=False)
    blocked = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "short_base64": self.short_base64,
            "long_url": self.long_url,
            "blocked": self.blocked,
            "created_at": self.created_at
        }