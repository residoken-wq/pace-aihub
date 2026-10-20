from enum import StrEnum

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


class ErrorCode(StrEnum):
    """Only codes listed in docs/specs/04_API_GATEWAY.md. New codes need an ADR."""

    UNAUTHENTICATED = "UNAUTHENTICATED"
    WORKSPACE_FORBIDDEN = "WORKSPACE_FORBIDDEN"
    DUPLICATE_RUN = "DUPLICATE_RUN"
    INVALID_SOURCE_CONFIG = "INVALID_SOURCE_CONFIG"
    BUDGET_EXCEEDED = "BUDGET_EXCEEDED"
    PROVIDER_RATE_LIMIT = "PROVIDER_RATE_LIMIT"
    MODEL_RESPONSE_INVALID = "MODEL_RESPONSE_INVALID"
    CONNECTOR_UNAVAILABLE = "CONNECTOR_UNAVAILABLE"


ERROR_STATUS: dict[ErrorCode, int] = {
    ErrorCode.UNAUTHENTICATED: 401,
    ErrorCode.WORKSPACE_FORBIDDEN: 403,
    ErrorCode.DUPLICATE_RUN: 409,
    ErrorCode.INVALID_SOURCE_CONFIG: 422,
    ErrorCode.BUDGET_EXCEEDED: 429,
    ErrorCode.PROVIDER_RATE_LIMIT: 429,
    ErrorCode.MODEL_RESPONSE_INVALID: 502,
    ErrorCode.CONNECTOR_UNAVAILABLE: 503,
}


class ApiError(Exception):
    def __init__(self, code: ErrorCode, message: str) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.status_code = ERROR_STATUS[code]


def error_body(code: ErrorCode, message: str, request_id: str | None) -> dict[str, object]:
    return {"error": {"code": code.value, "message": message, "request_id": request_id}}


async def _api_error_handler(request: Request, exc: Exception) -> JSONResponse:
    if not isinstance(exc, ApiError):  # registered for ApiError only
        raise exc
    request_id = getattr(request.state, "request_id", None)
    return JSONResponse(
        status_code=exc.status_code, content=error_body(exc.code, exc.message, request_id)
    )


def register_error_handlers(app: FastAPI) -> None:
    app.add_exception_handler(ApiError, _api_error_handler)
