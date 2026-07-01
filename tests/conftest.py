"""Shared test fixtures.

The tests exercise the public ``api_router`` in isolation. We mount it on a
fresh ``FastAPI`` instance at the ``/api`` prefix (mirroring ``zws/app.py``)
instead of importing ``zws.app.app`` directly, so the app's ``on_startup``
``init_db()`` hook (which touches the database) is never triggered. The Hello
World endpoint has no database dependency, so this keeps the tests fast and
hermetic.
"""

import pytest
import pytest_asyncio
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from zws.routes.api import api_router


@pytest.fixture(scope="session")
def app() -> FastAPI:
    test_app = FastAPI()
    test_app.include_router(api_router, prefix="/api", tags=["API"])
    return test_app


@pytest_asyncio.fixture
async def client(app: FastAPI) -> AsyncClient:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
