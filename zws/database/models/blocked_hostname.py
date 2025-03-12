from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class BlockedHostname(Base):
    __tablename__ = 'blocked_hostnames'

    id = Column(Integer, primary_key=True, autoincrement=True)
    hostname = Column(String, nullable=False)
    domain_name = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.now, nullable=False)

    def __init__(self, hostname, domain_name):
        if not isinstance(hostname, str) or not hostname.strip():
            raise ValueError("Hostname must be a non-empty string")
        if not isinstance(domain_name, str):
            raise ValueError("Domain name must be a string")
        if domain_name.strip() == "":
            self.domain_name = None
        else:
            self.domain_name = domain_name
        self.hostname = hostname

    def __repr__(self):
        return f'BlockedHostname(id={self.id}, hostname={self.hostname}, domain_name={self.domain_name}, created_at={self.created_at})'