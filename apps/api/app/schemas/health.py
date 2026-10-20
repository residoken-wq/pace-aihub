from typing import Literal

from pydantic import BaseModel

CheckStatus = Literal["ok", "down"]


class Liveness(BaseModel):
    status: Literal["ok"] = "ok"


class Readiness(BaseModel):
    status: Literal["ready", "not_ready"]
    checks: dict[str, CheckStatus]
