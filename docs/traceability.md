# Traceability matrix

| Story | FR / Rule | Files (main) | Tests | UAT | Status | Phase |
|---|---|---|---|---|---|---|
| INF-01 | NFR | infra/, .github/, apps/api (health, request_id, errors, logging), apps/worker (queues), packages/contracts | apps/api/tests (health, readiness, request_id, errors, logging redaction, migrations up/down/up), apps/worker/tests (config, ping round-trip); ci pipeline, deploy smoke | — | In progress (INF-01a PR-A) | 1/4 |
| UI-00 | 05 design system (ADR-014) | apps/web/components/ui, patterns | component tests | — | Not started | 1 |
| AUTH-01 | FR-01, ADR-013 §4 | apps/api/app/routers/auth.py, migration `user_sessions` (mới, thay đổi so với 03_DATABASE_SCHEMA) | tests/api/test_auth.py | UAT-08, UAT-11 | Not started | 1 |
| DB-01 | — | apps/api/migrations/ | tests/db/ | — | Not started | 1 |
| TOOL-01 | FR-02 | | | UAT-01 | Not started | 2 |
| UI-01 | FR-02, O1 | | | UAT-01 | Not started | 2 |
| COL-01 | FR-03 | | | UAT-02, UAT-04 | Not started | 2 |
| GW-01 | FR-05 | | | — | Not started | 2 |
| AI-01 | FR-06, FR-07 | | | UAT-05, UAT-06 | Not started | 2 |
| RUN-01 | FR-04 | | | UAT-03 | Not started | 2/3 |
| RPT-01 | FR-10 | | | UAT-07 | Not started | 2/3 |
| GW-02 | FR-09 | | | UAT-09, UAT-12 | Not started | 3 |
| COL-02 | FR-03 | | | UAT-02 | Not started | 3 |
| OUT-01 | FR-08 | | | UAT-07, UAT-10 | Not started | 3 |
| OBS-01 | FR-10 | | | — | Not started | 3 |
| CMS-01 | FR-09, FR-10 (ADR-014) | | | UAT-09, UAT-11 | Not started | 3 |
| QA-01 | all | | | all | Not started | 4 |
