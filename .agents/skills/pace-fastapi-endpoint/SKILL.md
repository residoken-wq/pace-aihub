---
name: pace-fastapi-endpoint
description: Create or change a PACE AI Hub REST endpoint in apps/api (FastAPI) with workspace RBAC, standard errors, idempotency, audit and tests. Use whenever adding/modifying an /api/v1 route, service or repository.
---
# New/changed API endpoint

1. Confirm the contract in `docs/specs/04_API_GATEWAY.md` (path, method, role, request/response, error codes). If missing, draft it and ask the user before coding.
2. Create/modify in this order:
   - `app/schemas/<domain>.py` — Pydantic v2 request/response (`model_config = ConfigDict(extra="forbid")`).
   - `app/repositories/<domain>.py` — every method takes `workspace_id`; queries filter by it.
   - `app/services/<domain>.py` — business rules, transaction boundaries, audit event.
   - `app/routers/<domain>.py` — thin; deps `current_user`, `require_workspace_role(...)`; map domain errors → `ApiError(code)`.
3. Template (adapt):
```python
@router.post("/tools/{tool_id}/runs", status_code=202, response_model=RunAccepted)
async def create_run(
    tool_id: UUID,
    body: CreateRunRequest,
    user: User = Depends(current_user),
    db: AsyncSession = Depends(get_db),
):
    tool = await tools_repo.get_for_user(db, tool_id, user.id)        # 404 if not visible
    await require_role(db, user.id, tool.workspace_id, Role.member)    # 403 WORKSPACE_FORBIDDEN
    run = await runs_service.enqueue(db, tool, body.tool_version_id,
                                     body.mode, body.idempotency_key, user)  # 409 DUPLICATE_RUN
    return RunAccepted(run_id=run.id, status=run.status)
```
4. Tests (`tests/api/test_<domain>.py`, real Postgres via testcontainers): 201/202 happy path · 401 no session · 403 member of other workspace · 422 invalid body · domain error codes (409/429…) · idempotent replay returns same resource · audit row written.
5. Regenerate OpenAPI → `packages/contracts/openapi.yaml`, then `pnpm contracts:gen`.
