from sqlalchemy.orm import Session
from zws.database.models.url_model import BlockedHostname

class BlockedHostnamesRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all_blocked_hostnames(self):
        return self.db.query(BlockedHostname).all()