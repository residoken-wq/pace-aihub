from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from app.core.errors import ERROR_STATUS, ApiError, ErrorCode


async def test_api_error_uses_envelope_with_request_id(app: FastAPI) -> None:
    @app.get("/boom")
    async def boom() -> None:
        raise ApiError(ErrorCode.WORKSPACE_FORBIDDEN, "Không có quyền truy cập workspace này.")

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        res = await c.get("/boom", headers={"x-request-id": "req-12345678"})

    assert res.status_code == 403
    assert res.json() == {
        "error": {
            "code": "WORKSPACE_FORBIDDEN",
            "message": "Không có quyền truy cập workspace này.",
            "request_id": "req-12345678",
        }
    }


def test_every_spec_code_has_a_status() -> None:
    assert set(ERROR_STATUS) == set(ErrorCode)
    assert ERROR_STATUS[ErrorCode.UNAUTHENTICATED] == 401
    assert ERROR_STATUS[ErrorCode.BUDGET_EXCEEDED] == 429
