import asyncio

import pytest
from fastapi import FastAPI
from httpx import AsyncClient

from tests.conftest import FAKE_DB_PASSWORD, FAKE_DB_URL


async def test_healthz_ok(client: AsyncClient) -> None:
    res = await client.get("/healthz")
    assert res.status_code == 200
    assert res.json() == {"status": "ok"}


async def test_readyz_ready_when_all_dependencies_up(client: AsyncClient) -> None:
    res = await client.get("/readyz")
    assert res.status_code == 200
    assert res.json() == {"status": "ready", "checks": {"postgres": "ok", "valkey": "ok"}}


async def test_readyz_503_when_postgres_down_and_no_secret_leak(
    app: FastAPI, client: AsyncClient, capsys: pytest.CaptureFixture[str]
) -> None:
    async def failing_probe() -> None:
        # Drivers often put the DSN in the error text; it must not reach the body or logs.
        raise ConnectionRefusedError(f"could not connect to {FAKE_DB_URL}")

    app.state.readiness_probes["postgres"] = failing_probe

    res = await client.get("/readyz")

    assert res.status_code == 503
    assert res.json() == {"status": "not_ready", "checks": {"postgres": "down", "valkey": "ok"}}
    assert FAKE_DB_PASSWORD not in res.text
    out = capsys.readouterr()
    assert "readiness_check_failed" in out.out + out.err
    assert FAKE_DB_PASSWORD not in out.out + out.err


async def test_readyz_503_when_probe_hangs(app: FastAPI, client: AsyncClient) -> None:
    async def hanging_probe() -> None:
        await asyncio.sleep(10)

    app.state.readiness_probes["valkey"] = hanging_probe

    res = await client.get("/readyz")

    assert res.status_code == 503
    assert res.json()["checks"]["valkey"] == "down"
