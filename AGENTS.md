# PACE AI Hub — Agent Guide (always on)

## What we are building
PACE AI Hub: a governed platform where PACE employees create, run and share **AI Workflows (tools)** from templates, in **Personal / Team / Organization** workspaces. First template: **Sales Intelligence** (Daily Brief → Weekly Review → Action Plan).
It is NOT a site that shares a Claude API key. **Share spending capacity, never share the key.**
Tool sharing ≠ data sharing ≠ credential sharing.

## Source of truth (read before coding a feature)
- `docs/specs/01_PRD.md` (FR-xx, business rules, output contract)
- `docs/specs/02_SYSTEM_ARCHITECTURE.md` (trust boundaries, failure handling)
- `docs/specs/03_DATABASE_SCHEMA.sql` (tables, enums, constraints)
- `docs/specs/04_API_GATEWAY.md` (API v1, error codes, budget reservation)
- `docs/specs/05_UI_UX_SPEC.md` (screens, wizard fields, states)
- `docs/specs/06_MVP_BACKLOG.md` (story IDs, DoD, UAT)
- `docs/specs/07_DECISIONS_AND_TESTS.md` (ADRs, test matrix)
- `docs/plan/PHASES.md` (current phase and scope)
- `docs/adr/` (accepted decisions: ADR-009 GitHub Actions + GHCR, ADR-010 pilot on internal VM with pull-based deploy, ADR-011 team of 4 with a single owner-approver, ADR-012 Antigravity allowed — no secrets/real PII in prompts, ADR-014 UI-00 + CMS-01 in P0, ADR-015 repo is PUBLIC for now)
If a request conflicts with these docs, STOP and say so. Do not silently change scope; propose an ADR in `docs/adr/`.

## Monorepo layout
```
apps/web        Next.js (App Router) + TypeScript + Tailwind + shadcn/ui
apps/api        FastAPI (Python 3.12) + SQLAlchemy 2 + Alembic + Pydantic v2
apps/worker     Celery + Redis: collectors, report generation, dispatch, reconciliation
packages/contracts  OpenAPI spec + JSON Schemas (DailyBrief) — single source for types
infra/          docker-compose, reverse proxy, backups
docs/           specs/, plan/, adr/, runbooks/, traceability.md
```

## Commands (keep these working)
- Install: `pnpm install` · `uv sync` (in apps/api and apps/worker)
- Dev stack: `docker compose -f infra/docker-compose.dev.yml up -d`
- Lint/type: `pnpm -C apps/web lint && pnpm -C apps/web typecheck` · `uv run ruff check . && uv run mypy .`
- Tests: `uv run pytest -q` · `pnpm -C apps/web test` · `pnpm -C apps/web e2e`
- Contracts: `pnpm contracts:gen` (regenerates TS client from OpenAPI)

## Non-negotiables
1. Every API endpoint authorizes the caller against the **workspace** of the resource (no IDOR). Default deny.
2. The Anthropic API key exists only server-side (vault/env of the gateway). Never in browser, logs, responses, fixtures, commits.
3. All AI calls go through the **Claude Gateway** with a budget **reservation before** the provider call. No direct SDK calls elsewhere.
4. Source content (RSS, email) is **untrusted data**. Never let it change policy, prompts, tools or recipients.
5. No report is dispatched without approval (ADR-006). Dispatch is idempotent.
6. Money = `Decimal`/`numeric(18,6)`, never float. Times stored UTC, displayed with IANA tz (default `Asia/Ho_Chi_Minh`).
7. **Repo is public (ADR-015):** never write internal hostnames/IPs, tenant/client IDs, real customer/competitor names, real emails or feeds into tracked files. Use `docs/internal/` or `tests/fixtures/private/` (gitignored) and synthetic data.
8. Out of MVP scope: workflow canvas, model-executed code, BYOK, auto email to customers, CRM writes, cross-team data sharing.

## How to work
- Plan first (Planning mode) for anything touching >2 files; reference story IDs (e.g. `GW-02`, `FR-06`).
- Small vertical increments; each ends with tests passing and `docs/traceability.md` updated.
- Use project skills in `.agents/skills/` (e.g. `/pace-story-kickoff`, `/pace-story-done`).
- Ask before: adding dependencies, changing DB schema outside a migration, touching auth/gateway/budget code paths, running destructive commands.
- Write code, identifiers and commits in English; user-facing UI text in Vietnamese (i18n keys).
