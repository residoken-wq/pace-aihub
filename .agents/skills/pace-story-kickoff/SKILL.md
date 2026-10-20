---
name: pace-story-kickoff
description: Start work on a PACE AI Hub backlog story (IDs like AUTH-01, GW-02, UI-01). Use when the user says "start", "kickoff", "implement story X", or names a story ID. Produces an implementation plan with acceptance criteria and test list before any code is written.
---
# Story kickoff

Goal: turn a backlog ID into an approved, testable implementation plan. Do NOT write production code in this skill.

## Steps
1. Locate the story in `docs/specs/06_MVP_BACKLOG.md` and the phase in `docs/plan/PHASES.md`. If the story is not in the current phase, warn the user and ask to confirm.
2. Check dependencies (column "Depends on"). If a dependency is not done (see `docs/traceability.md`), stop and report.
3. Collect requirements: related FR-xx and business rules (`01_PRD.md`), tables (`03_DATABASE_SCHEMA.sql`), endpoints/error codes (`04_API_GATEWAY.md`), screens/states (`05_UI_UX_SPEC.md`), ADRs and test matrix rows (`07_DECISIONS_AND_TESTS.md`).
4. Write acceptance criteria as Given/When/Then (min. 1 happy path, 1 permission-denied, 1 failure/edge case). Mark any assumption as **ASSUMPTION** and any open question with who should answer (BA, IT, Sales, Data owner).
5. Produce the plan artifact with sections:
   - Scope / out of scope
   - Files to create/modify (paths)
   - Data/API/UI changes
   - Test list (unit, integration, e2e; map to UAT-xx where relevant)
   - Risks & security notes (IDOR, secrets, injection, money, idempotency)
   - Estimated slices (each ≤ ~half day, independently testable)
6. Ask the user to approve the plan. Only after approval, implement slice by slice, running tests after each.
7. When finished, run `/pace-story-done`.
