# Implementation Plan: Hello World Endpoint

**Ticket:** Implement hello word endpoint
**Goal:** Implement an unauthenticated `GET` endpoint that returns JSON with `msg = "Hello World"`.

## 1. Summary

Add a simple, public (no-auth) `GET` endpoint to the existing `zws` FastAPI
application that returns:

```json
{ "msg": "Hello World" }
```

This is a demo capability used to validate the end-to-end request/response flow
of the service.

## 2. Context & Stack

This repository is a **Python 3.12 / FastAPI** application (see `Pipfile`:
`fastapi`, `sqlalchemy`, `pydantic`, `uvicorn`). The app is defined in
`zws/app.py` and mounts an `api_router` (from `zws/routes/api.py`) under the
`/api` prefix.

> **Note on `node-programmer`:** The task instructions mention using the
> `node-programmer` agent for any Node.js work. This project contains **no
> Node.js code** (it is a pure Python/FastAPI service), so no Node.js work is
> required and that agent is not applicable here. API design decisions below
> follow the official `fastapi` skill conventions.

## 3. API Design

Following the existing routing convention (feature routers with their own
prefix/tags, aggregated by `api_router`, which is mounted at `/api`):

| Property        | Value                                  |
| --------------- | -------------------------------------- |
| Method          | `GET`                                  |
| Path            | `/api/hello`                           |
| Auth            | None (public)                          |
| Success status  | `200 OK`                               |
| Response model  | `HelloResponse` (`{ "msg": str }`)     |
| Response body   | `{ "msg": "Hello World" }`             |

### Design decisions (per FastAPI best practices)

- **Pydantic response model** — declare a `HelloResponse` model and use it as
  the function return type so FastAPI validates, filters, serializes (Pydantic
  in Rust), and documents the endpoint in OpenAPI.
- **Sync `def`** — the handler does no I/O and no blocking work; use a plain
  `def` handler (runs in the threadpool) rather than `async def`.
- **Router-level `prefix`/`tags`** — set `prefix="/hello"` and
  `tags=["hello"]` on the `APIRouter` itself, not in `include_router()`,
  matching the skill guidance and the existing `blocked_router` structure.
- **No dependencies / no DB** — the endpoint is stateless; it does not touch the
  database or any service layer.

## 4. Files to Add / Change

1. **`zws/schemas/hello_schema.py`** (new) — Pydantic response model:
   ```python
   from pydantic import BaseModel

   class HelloResponse(BaseModel):
       msg: str
   ```

2. **`zws/routes/hello.py`** (new) — the hello router:
   ```python
   from fastapi import APIRouter

   from zws.schemas.hello_schema import HelloResponse

   hello_router = APIRouter(prefix="/hello", tags=["hello"])

   @hello_router.get("/")
   def hello() -> HelloResponse:
       return HelloResponse(msg="Hello World")
   ```

3. **`zws/routes/api.py`** (change) — register the new router on `api_router`:
   ```python
   from zws.routes.hello import hello_router
   ...
   api_router.include_router(hello_router)
   ```
   (Prefix/tags already live on `hello_router`, keeping `include_router` clean.)

Resulting full path: **`GET /api/hello/`**.

## 5. Testing / Verification

- Run the dev server (`uvicorn zws.app:app` or `fastapi dev zws/app.py`).
- `curl http://localhost:9997/api/hello/` returns `{"msg":"Hello World"}` with
  HTTP `200`.
- Confirm the endpoint appears in the OpenAPI docs at `/docs` under the
  `hello` tag with the `HelloResponse` schema.
- (Optional) Add a FastAPI `TestClient` test asserting status `200` and body
  `{"msg": "Hello World"}`.

## 6. Out of Scope

- Authentication / authorization (endpoint is intentionally public).
- Database access or persistence.
- Any Node.js / frontend work (not part of this repository).

## 7. Rollout

Small, additive change with no impact on existing routes. No migrations, config,
or dependency changes required.
