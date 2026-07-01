"""Async API tests for the public Hello World endpoint.

Endpoint under test: ``GET /api/hello/`` -> ``200 {"msg": "Hello World"}``
(public, no auth, no database).
"""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_hello_returns_200(client: AsyncClient) -> None:
    resp = await client.get("/api/hello/")
    assert resp.status_code == 200


@pytest.mark.asyncio
async def test_hello_returns_expected_body(client: AsyncClient) -> None:
    resp = await client.get("/api/hello/")
    assert resp.json() == {"msg": "Hello World"}


@pytest.mark.asyncio
async def test_hello_content_type_is_json(client: AsyncClient) -> None:
    resp = await client.get("/api/hello/")
    assert resp.headers["content-type"].startswith("application/json")


@pytest.mark.asyncio
async def test_hello_response_shape(client: AsyncClient) -> None:
    """Response matches the HelloResponse schema: single string field `msg`."""
    body = (await client.get("/api/hello/")).json()
    assert set(body.keys()) == {"msg"}
    assert isinstance(body["msg"], str)


@pytest.mark.asyncio
async def test_hello_requires_no_auth(client: AsyncClient) -> None:
    """Endpoint is public: no Authorization header is needed for a 200."""
    resp = await client.get("/api/hello/")
    assert resp.status_code == 200
    assert "www-authenticate" not in resp.headers


@pytest.mark.asyncio
async def test_hello_only_get_allowed(client: AsyncClient) -> None:
    """A non-GET verb on the route is rejected (405)."""
    resp = await client.post("/api/hello/")
    assert resp.status_code == 405


@pytest.mark.asyncio
async def test_hello_registered_in_openapi(client: AsyncClient) -> None:
    """The endpoint is documented in the OpenAPI schema under the hello tag."""
    schema = (await client.get("/openapi.json")).json()
    assert "/api/hello/" in schema["paths"]
    assert "get" in schema["paths"]["/api/hello/"]
