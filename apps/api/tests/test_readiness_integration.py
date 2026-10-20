import pytest
from httpx import ASGITransport, AsyncClient
from pydantic import SecretStr

from app.core.config import Settings
from app.main import create_app
from tests.docker_support import POSTGRES_IMAGE, docker_available, valkey_url

pytestmark = [
    pytest.mark.integration,
    pytest.mark.skipif(not docker_available(), reason="Docker not available"),
]


async def test_readyz_against_real_postgres_and_valkey() -> None:
    from testcontainers.postgres import PostgresContainer

    with PostgresContainer(POSTGRES_IMAGE, driver="asyncpg") as pg, valkey_url() as vk_url:
        settings = Settings(
            env="test",
            database_url=SecretStr(pg.get_connection_url()),
            valkey_url=SecretStr(vk_url),
        )
        app = create_app(settings)
        async with (
            app.router.lifespan_context(app),
            AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c,
        ):
            res = await c.get("/readyz")

    assert res.status_code == 200
    assert res.json()["status"] == "ready"
