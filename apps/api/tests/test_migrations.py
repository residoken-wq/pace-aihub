import pytest
from alembic import command
from alembic.config import Config

from tests.docker_support import POSTGRES_IMAGE, docker_available

pytestmark = [
    pytest.mark.integration,
    pytest.mark.skipif(not docker_available(), reason="Docker not available"),
]


def test_migrations_up_down_up() -> None:
    from testcontainers.postgres import PostgresContainer

    with PostgresContainer(POSTGRES_IMAGE, driver="asyncpg") as pg:
        cfg = Config("alembic.ini")
        cfg.attributes["database_url"] = pg.get_connection_url()
        command.upgrade(cfg, "head")
        command.downgrade(cfg, "base")
        command.upgrade(cfg, "head")
