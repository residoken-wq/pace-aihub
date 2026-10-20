---
name: pace-deploy-vm
description: Prepare or change deployment of PACE AI Hub to the internal pilot VM (Ubuntu 24.04, Docker Compose, pull-based from GHCR) — compose.prod, reverse proxy/TLS, env/secrets layout, deploy and rollback scripts, backups, egress allowlist, health checks. Use for INF-01c (walking skeleton in Phase 1), INF-01b (hardening in Phase 4), release preparation, or any deploy/ops change.
---
# Deploy to internal VM (ADR-009, ADR-010)

Model: **pull-based**. GitHub Actions builds and pushes signed images to GHCR; the VM pulls a specific tag. No inbound access from GitHub to the internal network. A self-hosted runner is only allowed if IT approves (ephemeral, non-root, this private repo only).

## Files to produce (`infra/`)
- `compose.prod.yml`: services `proxy` (Caddy or Nginx, TLS), `web`, `api`, `worker`, `beat`, `redis` (AOF on), `postgres:16` (or external DB VM), optional `pgbackup`. Images pinned by tag `sha-<short>` from `.env.release`. Healthchecks, `restart: unless-stopped`, resource limits, read-only root fs where possible, non-root users, internal network for db/redis (not published).
- `deploy/deploy.sh <tag>`: verify image signature/digest → `docker compose pull` → run `alembic upgrade head` as one-off job → `up -d` → wait for `/readyz` → smoke test → record release in `deploy/releases.log`. Abort on any failure.
- `deploy/rollback.sh <previous-tag>`: re-deploy previous tag; DB rollback only if the migration is marked reversible and a human confirms.
- `deploy/backup.sh` + systemd timer: `pg_dump -Fc` encrypted (age/gpg) → off-VM storage; retention per data policy; `deploy/restore-test.sh` restores into a scratch DB and runs sanity queries.
- `env/` layout on VM: `/etc/pace-ai-hub/*.env` (root:pace 0640), never committed; `.env.example` documents keys only. Anthropic key, Entra secret, DB password from IT secret store.
- `docs/runbooks/`: deploy, rollback, backup/restore, rotate secrets, revoke user, budget 100%, DLQ handling, VM egress list.

## Checks before declaring done
1. Egress test from VM: reachable `api.anthropic.com`, `login.microsoftonline.com`, `graph.microsoft.com`, `ghcr.io`, approved RSS hosts; blocked: arbitrary internet, RFC1918 from collectors.
2. TLS valid on internal domain; HSTS; Entra redirect URI matches.
3. `docker compose ps` all healthy; `/healthz` and `/readyz` OK; worker consumes test job; beat schedules once (no duplicate slot).
4. Restore test passes; rollback to previous tag rehearsed.
5. No secret values in images (`trivy`/`docker history` check), logs, or repo.
Ask the user before any command that touches the real VM.
