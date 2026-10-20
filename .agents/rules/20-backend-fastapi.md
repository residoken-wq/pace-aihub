---
trigger: glob
globs: apps/api/**, apps/worker/**
---
# Backend conventions (FastAPI / Celery)

- Python 3.12, `uv`, `ruff` (lint+format), `mypy --strict` on `app/`.
- Layering: `routers/` (HTTP only) → `services/` (business rules, transactions) → `repositories/` (SQLAlchemy 2.0 typed, always workspace-scoped) → `models/`. Schemas in `schemas/` (Pydantic v2). No DB access in routers.
- Dependency `get_current_user` + `require_workspace_role(min_role)`; every router uses them.
- API prefix `/api/v1`. Error body: `{"error": {"code": "BUDGET_EXCEEDED", "message": "...", "request_id": "..."}}`. Use only codes from `docs/specs/04_API_GATEWAY.md`; add new ones via ADR.
- Long work returns `202 {run_id, status}` and is queued to the worker. Accept `idempotency_key` on create-run and dispatch.
- Transactions: budget reservation uses `SELECT ... FOR UPDATE` on `budget_periods`, commit BEFORE calling the provider. Settlement in its own transaction, append-only `usage_ledger`.
- Worker tasks: idempotent, bounded retries with exponential backoff + jitter, `acks_late`, visibility timeout, DLQ queue. Re-use `run_id` on retry.
- Schedules: unique `(tool_id, schedule_slot)`; compute slots in IANA tz; Monday lookback from Friday 08:00 local (configurable).
- Tests: `pytest`, `httpx.AsyncClient`, testcontainers Postgres (no SQLite for tenant/locking tests). Each endpoint: happy path, 401, 403 cross-workspace, validation 422.
- Update `packages/contracts/openapi.yaml` when routes change (generate from FastAPI, commit the diff).
