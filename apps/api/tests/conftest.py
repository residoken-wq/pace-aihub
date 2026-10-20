from collections.abc import AsyncIterator

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from pydantic import SecretStr

from app.core.config import Settings
from app.main import create_app
from app.services.health import Probe

# Fake credentials so tests can prove they never leak into responses or logs.
FAKE_DB_PASSWORD = "fake-db-pass-123"
FAKE_DB_URL = f"postgresql+asyncpg://pace:{FAKE_DB_PASSWORD}@db.invalid:5432/pace"


@pytest.fixture
def settings() -> Settings:
    return Settings(
        env="test",
        database_url=SecretStr(FAKE_DB_URL),
        valkey_url=SecretStr("redis://valkey.invalid:6379/0"),
        readiness_timeout_s=0.5,
    )


async def ok_probe() -> None:
    return None


@pytest.fixture
def app(settings: Settings) -> FastAPI:
    app = create_app(settings)
    # ASGITransport does not run lifespan; inject probes directly.
    probes: dict[str, Probe] = {"postgres": ok_probe, "valkey": ok_probe}
    app.state.readiness_probes = probes
    return app


@pytest.fixture
async def client(app: FastAPI) -> AsyncIterator[AsyncClient]:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c
