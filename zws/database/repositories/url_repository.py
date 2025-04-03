package zws.database.repositories

from sqlalchemy import insert, select
from zws.database.models.blocked_hostname import BlockedHostname
from sqlalchemy.exc import SQLAlchemyError

class UrlRepository:
    def __init__(self, database):
        self.database = database

    async def insert_url(self, url_object: BlockedHostname, short_id: str):
        if not self.database:
            raise Exception("Database connection is not established")
        try:
            existing_url_query = select(BlockedHostname).where(BlockedHostname.url == url_object.url)
            existing_url = await self.database.fetch_one(existing_url_query)
            if existing_url:
                raise Exception("URL already exists")
            query = insert(BlockedHostname).values(url=url_object.url, short_id=short_id)
            await self.database.execute(query)
        except SQLAlchemyError as e:
            raise Exception("Database insertion error") from e

    async def is_url_blocked(self, url_object: BlockedHostname) -> bool:
        if not self.database:
            raise Exception("Database connection is not established")
        try:
            query = select(BlockedHostname).where(BlockedHostname.url == url_object.url)
            result = await self.database.fetch_one(query)
            return result is not None
        except SQLAlchemyError as e:
            raise Exception("Database query error") from e