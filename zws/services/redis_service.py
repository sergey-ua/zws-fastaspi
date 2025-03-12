```python
import redis
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String

Base = declarative_base()

class BlockedHostname(Base):
    __tablename__ = 'blocked_hostnames'
    hostname = Column(String, primary_key=True)

BLOCKED_HOSTNAMES_REDIS_KEY = 'blocked_hostnames'
BLOCKED_HOSTNAMES_CACHE_DURATION = 3600  # 1 hour

class RedisService:
    def __init__(self, redis_client, db_session):
        self.redis_client = redis_client
        self.db_session = db_session

    def redis_contains_hostnames(self, hostname: str) -> bool:
        return self.redis_client.sismember(BLOCKED_HOSTNAMES_REDIS_KEY, hostname)

    def populate_redis_cache(self) -> None:
        blocked_hostnames = self.db_session.query(BlockedHostname).all()
        for blocked_hostname in blocked_hostnames:
            self.redis_client.sadd(BLOCKED_HOSTNAMES_REDIS_KEY, blocked_hostname.hostname)
        self.redis_client.expire(BLOCKED_HOSTNAMES_REDIS_KEY, BLOCKED_HOSTNAMES_CACHE_DURATION)
```