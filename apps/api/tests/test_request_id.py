import uuid

from httpx import AsyncClient


async def test_generates_request_id(client: AsyncClient) -> None:
    res = await client.get("/healthz")
    uuid.UUID(res.headers["x-request-id"])


async def test_echoes_valid_incoming_request_id(client: AsyncClient) -> None:
    res = await client.get("/healthz", headers={"x-request-id": "abc-12345678"})
    assert res.headers["x-request-id"] == "abc-12345678"


async def test_replaces_unsafe_incoming_request_id(client: AsyncClient) -> None:
    res = await client.get("/healthz", headers={"x-request-id": "bad id\twith<script>"})
    uuid.UUID(res.headers["x-request-id"])
