import asyncio
from collections.abc import Awaitable, Callable

import structlog
from redis.asyncio import Redis
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine

from app.schemas.health import CheckStatus, Readiness

log = structlog.get_logger(__name__)

Probe = Callable[[], Awaitable[None]]


def postgres_probe(engine: AsyncEngine) -> Probe:
    async def probe() -> None:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))

    return probe


def valkey_probe(client: Redis) -> Probe:
    async def probe() -> None:
        await client.ping()

    return probe


async def _run(name: str, probe: Probe, timeout_s: float) -> CheckStatus:
    try:
        await asyncio.wait_for(probe(), timeout=timeout_s)
    except Exception as exc:
        # Log only the exception type: driver messages can embed the connection URL.
        log.warning("readiness_check_failed", check=name, error_type=type(exc).__name__)
        return "down"
    return "ok"


async def check_readiness(probes: dict[str, Probe], timeout_s: float) -> Readiness:
    names = list(probes)
    results = await asyncio.gather(*(_run(n, probes[n], timeout_s) for n in names))
    checks = dict(zip(names, results, strict=True))
    status = "ready" if all(r == "ok" for r in results) else "not_ready"
    return Readiness(status=status, checks=checks)
