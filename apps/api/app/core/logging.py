import logging
import re
from collections.abc import Mapping, MutableMapping
from typing import Any

import structlog

REDACTED = "[REDACTED]"

_SENSITIVE_KEY = re.compile(
    r"(authorization|cookie|token|secret|password|passwd|api[_-]?key|credential|dsn|database_url|valkey_url)",
    re.IGNORECASE,
)
# Values that look like credentials even when logged under an innocent key.
_SENSITIVE_VALUE = re.compile(
    r"(sk-ant-[A-Za-z0-9_\-]+|Bearer\s+[A-Za-z0-9._\-]+|://[^/\s:@]+:[^@\s]+@)",
)


def _redact_value(value: Any) -> Any:
    if isinstance(value, str):
        return _SENSITIVE_VALUE.sub(REDACTED, value)
    if isinstance(value, Mapping):
        return _redact_mapping(value)
    if isinstance(value, list | tuple):
        return type(value)(_redact_value(v) for v in value)
    return value


def _redact_mapping(data: Mapping[str, Any]) -> dict[str, Any]:
    return {
        k: REDACTED if _SENSITIVE_KEY.search(str(k)) else _redact_value(v) for k, v in data.items()
    }


def redact_processor(
    _logger: Any, _method: str, event_dict: MutableMapping[str, Any]
) -> MutableMapping[str, Any]:
    """structlog processor: drop secrets/PII-bearing fields before rendering (10-security.md)."""
    return _redact_mapping(event_dict)


def configure_logging(level: str = "INFO") -> None:
    logging.basicConfig(format="%(message)s", level=level)
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso", utc=True),
            redact_processor,
            structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(logging.getLevelName(level)),
        cache_logger_on_first_use=True,
    )
