package zws.services

import base64
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, insert
from zws.database.models.url_model import UrlModel
from zws.database.models.visit_model import VisitModel

class UrlsService:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def retrieve_url(self, short: str):
        encoded_short = base64.b64encode(short.encode()).decode()
        try:
            async with self.db_session.begin():
                query = select(UrlModel.long_url, UrlModel.blocked).where(UrlModel.short_base64 == encoded_short).limit(1)
                result = await self.db_session.execute(query)
                record = result.one_or_none()
                if not record:
                    return None
                long_url, blocked = record
                if not blocked:
                    update_query = update(UrlModel).where(UrlModel.short_base64 == encoded_short, UrlModel.blocked != True).values(blocked=True)
                    await self.db_session.execute(update_query)
                return {"long_url": long_url, "blocked": blocked}
        except SQLAlchemyError:
            await self.db_session.rollback()
            raise

    async def track_url_visit(self, short: str):
        encoded_short = base64.b64encode(short.encode()).decode()
        try:
            async with self.db_session.begin():
                query = select(UrlModel.id).where(UrlModel.short_base64 == encoded_short)
                result = await self.db_session.execute(query)
                url_record = result.one_or_none()
                if not url_record:
                    raise Exception("URL not found, can't track visit")
                visit = {"url_short_base64": encoded_short, "timestamp": datetime.utcnow()}
                insert_query = insert(VisitModel).values(visit)
                await self.db_session.execute(insert_query)
        except SQLAlchemyError:
            await self.db_session.rollback()
            raise