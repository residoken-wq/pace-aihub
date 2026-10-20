---
name: pace-qa-testcases
description: Design and automate PACE AI Hub test cases (unit, integration, Playwright e2e, UAT, security, reliability) from acceptance criteria, the test matrix and UAT list. Use when writing tests, building a test plan, preparing UAT, or checking coverage of a story/phase.
---
# QA test design

## Sources
- AC in the story plan; test matrix + gateway tests in `docs/specs/07_DECISIONS_AND_TESTS.md` and `04_API_GATEWAY.md`; UAT-01..12 in `06_MVP_BACKLOG.md`.

## Steps
1. Build a case table in `docs/qa/<story-or-phase>.md`:
   `TC-ID | Story/FR | Type (unit/int/e2e/sec/rel/uat) | Preconditions | Data | Steps | Expected | Priority | Automated (path)`.
2. Apply techniques: equivalence + boundary (5 items/group, 80%/100% budget, Monday 08:00 boundary, DST-free tz), state transitions (tool: draft→published→paused→archived; report: draft→pending_approval→approved/rejected→sent), negative/permission (each role × action), concurrency (quota race, duplicate schedule slot), idempotency (retry dispatch).
3. Automate: pytest for backend (`tests/…`, mark `@pytest.mark.uat("UAT-08")`), Playwright for UI flows (`apps/web/e2e/uat-xx-*.spec.ts`, test title starts with UAT ID), seed via API fixtures not UI clicks.
4. AI quality: golden set of ≥20 anonymized source bundles in `tests/golden/`; rubric (relevance, source correctness, fact/inference separation, actionability, Vietnamese quality — 1..5) and automatic checks (schema, no unknown source_ids, ≤5 items, empty-group note).
5. Report coverage: every AC and UAT → at least one automated test; list gaps and risks.

## UAT map
UAT-01 create tool ≤10 min · 02 duplicate URL skipped · 03 Monday lookback · 04 no source → explicit no updates · 05 3 groups ≤5 items · 06 source links + labels · 07 approval before email · 08 cross-team forbidden · 09 exhausted budget blocks · 10 retry no duplicate email · 11 revoked member blocked · 12 usage matches ledger.
