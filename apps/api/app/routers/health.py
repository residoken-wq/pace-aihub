from fastapi import APIRouter, Request, Response

from app.schemas.health import Liveness, Readiness
from app.services.health import check_readiness

# Probes are unauthenticated by design and expose no tenant data.
router = APIRouter(tags=["health"])


@router.get("/healthz", response_model=Liveness)
async def healthz() -> Liveness:
    return Liveness()


@router.get("/readyz", response_model=Readiness, responses={503: {"model": Readiness}})
async def readyz(request: Request, response: Response) -> Readiness:
    result = await check_readiness(
        request.app.state.readiness_probes, request.app.state.settings.readiness_timeout_s
    )
    if result.status != "ready":
        response.status_code = 503
    return result
