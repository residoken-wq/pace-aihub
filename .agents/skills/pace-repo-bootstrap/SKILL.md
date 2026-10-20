---
name: pace-repo-bootstrap
description: Scaffold the PACE AI Hub monorepo (Phase 1 / INF-01) — Next.js web, FastAPI api, Celery worker, contracts package, docker-compose dev stack, CI, pre-commit, gitleaks. Use only when the repo is empty or the user asks to bootstrap/scaffold the project.
---
# Repo bootstrap (run once)

Ask before installing anything. NEVER pin versions from memory — query the registry (`npm view <pkg> version`, `pip index versions <pkg>` / PyPI) at bootstrap time and pin the latest patch. Libraries without an LTS policy are 'rolling' (only latest is patched) — do not invent EOL dates. Baseline: Node 24 LTS, Next.js 16.x, Tailwind v4, Valkey (not Redis), PostgreSQL 17+. Use pinned, current stable versions and record them in `docs/adr/ADR-013-tech-stack.md`. Accepted decisions: `docs/adr/ADR-009-015-decisions.md` (GitHub Actions, internal VM pilot, team of 4, Antigravity allowed).

1. Root: `pnpm-workspace.yaml` (apps/web, packages/*), `.editorconfig`, `.gitignore` (env files, `.venv`, `node_modules`, `.next`), `.env.example` (no real values), `README.md`, `Makefile` or root `package.json` scripts matching AGENTS.md commands.
2. `apps/web`: **Next.js 16.x (latest patch)** via `create-next-app` (TS, App Router, Tailwind v4, ESLint, src dir off) — never Next.js 14 (EOL 26/10/2025) or 15 (EOL 21/10/2026); shadcn init, apply `pace-design-system` tokens, Roboto vi subset, AppShell with sidebar per spec, i18n (`next-intl`, `vi` default), TanStack Query provider, Vitest + Testing Library, Playwright.
3. `apps/api`: `uv init`; FastAPI, uvicorn, SQLAlchemy[asyncio] 2, asyncpg, alembic, pydantic-settings, structlog, httpx, authlib/msal (OIDC); dev: pytest, pytest-asyncio, testcontainers, ruff, mypy. Structure: `app/{routers,services,repositories,models,schemas,gateway,core}`; `/healthz`, `/readyz`; error envelope; request_id middleware; log redaction filter.
4. `apps/worker`: Celery + Valkey (Redis protocol), queues `collect`, `analyze`, `dispatch`, `reconcile`, `dlq`; beat schedule for reconciliation; shares models package with api (`packages/py-core` or path dependency).
5. Baseline migration from `docs/specs/03_DATABASE_SCHEMA.sql` via `pace-db-migration`.
6. `packages/contracts`: `openapi.yaml` (generated), `schemas/daily_brief.schema.json` (copy from `pace-claude-gateway/references`), TS client generation script (`openapi-typescript` or `orval`).
7. `infra/docker-compose.dev.yml`: postgres (major per ADR-013), valkey (per ADR-013), api, worker, web, mailpit (fake SMTP for dev). Healthchecks. Named volumes.
8. CI = **GitHub Actions** (ADR-009), GitHub-hosted runners, in `.github/workflows/`:
   - `ci.yml` (on PR + push to main): jobs `web` (lint, typecheck, vitest), `api` (ruff, mypy, pytest with `services:` postgres + valkey at ADR-013 versions), `migrations` (alembic up→down→up), `security` (gitleaks, `pnpm audit --prod`, `pip-audit`), `e2e` (Playwright against docker compose, upload report artifact). Use path filters, dependency caching, `concurrency` to cancel superseded runs.
   - `build.yml` (on main/tags): build api/worker/web images, trivy scan (fail on HIGH/CRITICAL), push to **GHCR** with tags `sha-<short>` and semver, sign/attest provenance if available.
   - Security defaults for every workflow: `permissions:` least privilege (default `contents: read`; `packages: write` only in build), pin third-party actions to full commit SHA, no secrets in PR jobs from forks, `pull_request` not `pull_request_target`.
   - Add `.github/dependabot.yml` (npm, pip/uv, github-actions, docker), `CODEOWNERS`, PR template with AC/test evidence checklist.
   - Deployment to the internal VM is NOT done here — see skill `pace-deploy-vm` (pull-based).
9. `pre-commit`: ruff, ruff-format, mypy (api), eslint, prettier, gitleaks.
10. Docs: `docs/traceability.md`, `docs/adr/0000-template.md`, `docs/runbooks/local-dev.md`.
Exit: `docker compose up` brings all services healthy; CI green on an empty feature; `/pace-story-done` passes for INF-01 (partial: TLS/backups in Phase 4).
