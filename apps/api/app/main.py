from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import Settings, get_settings
from app.core.db import create_engine
from app.core.errors import register_error_handlers
from app.core.logging import configure_logging
from app.core.request_id import RequestIdMiddleware
from app.core.valkey import create_valkey
from app.routers import health
from app.services.health import postgres_probe, valkey_probe


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or get_settings()
    configure_logging(settings.log_level)

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        engine = create_engine(settings)
        valkey = create_valkey(settings)
        app.state.readiness_probes = {
            "postgres": postgres_probe(engine),
            "valkey": valkey_probe(valkey),
        }
        try:
            yield
        finally:
            await valkey.aclose()
            await engine.dispose()

    app = FastAPI(title="PACE AI Hub API", version="0.1.0", lifespan=lifespan)
    app.state.settings = settings
    app.add_middleware(RequestIdMiddleware)
    register_error_handlers(app)
    app.include_router(health.router)
    return app
