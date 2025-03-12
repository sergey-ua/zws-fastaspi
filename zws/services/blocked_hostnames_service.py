```python
package zws.services

from zws.database.repositories import BlockedHostnamesRepository
from zws.database.repositories import UrlRepository
import redis
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from urllib.parse import urlparse
import json

class BlockedHostnamesService:
    def __init__(self):
        self.blocked_hostnames_repository = BlockedHostnamesRepository()
        self.redis_client = redis.Redis(host='localhost', port=6379, db=0)
        self.engine = create_engine('postgresql://user:password@host:port/dbname')
        self.Session = sessionmaker(bind=self.engine)
        self.validate_redis_configuration()

    def validate_redis_configuration(self):
        try:
            self.redis_client.ping()
        except redis.exceptions.ConnectionError as e:
            raise Exception(f"Redis connection error: {e}")

    def is_hostname_blocked(self, hostname):
        try:
            session = self.Session()
            blocked_hostnames = self.blocked_hostnames_repository.get_all_blocked_hostnames(session)
            session.close()
            if hostname in [blocked_hostname.hostname for blocked_hostname in blocked_hostnames]:
                return True
        except Exception as e:
            raise Exception(f"Error checking database: {e}")
        blocked_hostnames = self.redis_client.get('blocked_hostnames')
        if blocked_hostnames is None:
            try:
                session = self.Session()
                blocked_hostnames = self.blocked_hostnames_repository.get_all_blocked_hostnames(session)
                session.close()
                self.redis_client.set('blocked_hostnames', json.dumps([hostname.hostname for hostname in blocked_hostnames]))
            except Exception as e:
                raise Exception(f"Error populating Redis cache: {e}")
        if blocked_hostnames is not None:
            return hostname in json.loads(blocked_hostnames)
        return False

    def get_all_blocked_hostnames(self):
        try:
            session = self.Session()
            return self.blocked_hostnames_repository.get_all_blocked_hostnames(session)
        except Exception as e:
            raise Exception(f"Error retrieving blocked hostnames: {e}")

    def is_url_blocked(self, url):
        if not isinstance(url, str) or not url.startswith('http'):
            raise Exception("Invalid URL")
        try:
            hostname = urlparse(url).hostname
            return self.is_hostname_blocked(hostname)
        except Exception as e:
            raise Exception(f"Error parsing URL: {e}")
```