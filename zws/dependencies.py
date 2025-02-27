from contextlib import contextmanager

from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from zws.database.repositories.blocked_hostnames_repo import BlockedHostnamesRepository
from zws.services.blocked_hostnames_service import BlockedHostnamesService

DATABASE_URL = "sqlite:///./test.db"  # Replace with your actual database URL

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@contextmanager
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

def get_db_session() -> Session:
    with get_db() as db:
        return db

def get_blocked_hostnames_repo(db: Session = Depends(get_db_session)) -> BlockedHostnamesRepository:
    return BlockedHostnamesRepository(db)

def get_blocked_hostnames_service(
    blocked_hostnames_repo: BlockedHostnamesRepository = Depends(get_blocked_hostnames_repo)
) -> BlockedHostnamesService:
    return BlockedHostnamesService(blocked_hostnames_repo)