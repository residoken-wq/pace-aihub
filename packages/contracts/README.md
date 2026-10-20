# @pace/contracts

Single source for API types (AGENTS.md).

- `openapi.yaml`: generated from FastAPI (`apps/api/scripts/export_openapi.py`).
- `src/api.d.ts`: TypeScript types generated from `openapi.yaml` with `openapi-typescript`.
- `schemas/daily_brief.schema.json`: DailyBrief output contract (copied from `.agents/skills/pace-claude-gateway/references/`).

Regenerate after any API route change and commit the diff:

```bash
pnpm contracts:gen
```
