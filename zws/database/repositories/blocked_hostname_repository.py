package zws.database.repositories

from sqlalchemy.orm import Session
from zws.database.models.blocked_hostname import BlockedHostname

class BlockedHostnameRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def add_blocked_hostname(self, hostname: str):
        new_blocked_hostname = BlockedHostname(hostname=hostname)
        self.db_session.add(new_blocked_hostname)
        self.db_session.commit()

    def is_hostname_blocked(self, hostname: str) -> bool:
        return self.db_session.query(BlockedHostname).filter_by(hostname=hostname).first() is not None