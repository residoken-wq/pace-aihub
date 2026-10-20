---
name: pace-story-done
description: Verify a PACE AI Hub story against the Definition of Done and update traceability before commit/PR. Use when the user says "done", "finish", "ready for review", "create PR", or after implementing a story.
---
# Story done — verification

Run every step; report evidence. If any step fails, the story is NOT done — fix or report the blocker.

1. Run quality commands and paste summarized output:
   - `uv run ruff check . && uv run mypy . && uv run pytest -q` (api/worker, if touched)
   - `pnpm -C apps/web lint && pnpm -C apps/web typecheck && pnpm -C apps/web test` (web, if touched)
   - `pnpm -C apps/web e2e --grep "<UAT-ID>"` when a UAT flow is affected
   - `gitleaks detect --no-banner` (or `gitleaks protect --staged`)
2. Check each acceptance criterion → test name that proves it. List any AC without a test.
3. Security spot-check of the diff (`git diff main...`): workspace filter on new queries, role dependency on new routes, no secrets/PII in logs, no float money, untrusted input validated.
4. Contracts: if routes changed → regenerate OpenAPI and TS client, confirm no uncommitted diff. If models changed → migration exists and up/down passed.
5. UI: if screens changed → capture browser screenshots at 1440px and 390px, verify the 5 states, keyboard navigation and focus ring.
6. Update `docs/traceability.md`: `| Story | FR | Files | Tests | UAT | Status |`.
7. Draft a conventional commit / PR description: summary, story ID, AC checklist, test evidence, screenshots, risks, follow-ups.
