package zws.database.repositories

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from zws.database.models import BlockedHostname
import logging

class BlockedHostnamesRepository:
    def __init__(self, db_url):
        self.engine = create_engine(db_url)
        self.Session = sessionmaker(bind=self.engine)
        self.logger = logging.getLogger(__name__)

    def get_all_blocked_hostnames(self):
        try:
            session = self.Session()
            return session.query(BlockedHostname).all()
        except Exception as e:
            self.logger.error(f"Failed to retrieve all blocked hostnames: {str(e)}")
            raise
        finally:
            session.close()

    def get_blocked_hostname_by_id(self, id):
        try:
            session = self.Session()
            blocked_hostname = session.query(BlockedHostname).filter_by(id=id).first()
            if blocked_hostname is None:
                self.logger.error(f"Blocked hostname with id {id} does not exist")
                raise Exception(f"Blocked hostname with id {id} does not exist")
            return blocked_hostname
        except Exception as e:
            self.logger.error(f"Failed to retrieve blocked hostname by id {id}: {str(e)}")
            raise
        finally:
            session.close()

    def create_blocked_hostname(self, hostname):
        try:
            session = self.Session()
            existing_blocked_hostname = session.query(BlockedHostname).filter_by(hostname=hostname).first()
            if existing_blocked_hostname is not None:
                self.logger.error(f"Blocked hostname with name {hostname} already exists")
                raise Exception(f"Blocked hostname with name {hostname} already exists")
            blocked_hostname = BlockedHostname(hostname=hostname)
            session.add(blocked_hostname)
            session.commit()
            return blocked_hostname
        except Exception as e:
            session.rollback()
            self.logger.error(f"Failed to create blocked hostname {hostname}: {str(e)}")
            raise
        finally:
            session.close()