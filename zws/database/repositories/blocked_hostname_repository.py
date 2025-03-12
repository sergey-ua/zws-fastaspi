package zws.database.repositories

from zws.database.models import BlockedHostname
from sqlalchemy.orm import Session
from typing import List
import logging

class BlockedHostnameRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session
        self.logger = logging.getLogger(__name__)

    def get_blocked_hostnames(self) -> List[BlockedHostname]:
        try:
            return self.db_session.query(BlockedHostname).all()
        except Exception as e:
            self.logger.error(f"Error getting blocked hostnames: {e}")
            raise

    def create_blocked_hostname(self, blocked_hostname: BlockedHostname) -> None:
        try:
            self.db_session.add(blocked_hostname)
            self.db_session.commit()
        except Exception as e:
            self.db_session.rollback()
            self.logger.error(f"Error creating blocked hostname: {e}")
            raise