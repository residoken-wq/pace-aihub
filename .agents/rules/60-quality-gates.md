---
trigger: model_decision
description: Apply when finishing a task, preparing a commit/PR, or claiming a story is done. Defines Definition of Done and evidence required.
---
# Definition of Done (per story)

A story is done only when ALL hold — show evidence (command output, screenshot, test names):
1. Acceptance criteria (Given/When/Then) from the story are covered by automated tests that pass.
2. Lint, typecheck, unit + integration tests green; no new warnings ignored without comment.
3. Security checks relevant to the change: cross-workspace 403 test, no secret in diff (`gitleaks`), input validation.
4. API change → OpenAPI updated and TS client regenerated. Schema change → migration up/down tested.
5. UI change → 5 states implemented, keyboard + contrast checked, screenshots at 1440px and 390px.
6. `docs/traceability.md` row updated: Story ID → FR → files → tests → UAT ID.
7. Conventional commit message referencing story ID, e.g. `feat(gateway): atomic budget reservation [GW-02]`.
Never claim "done" or "tests pass" without having run them in this session.
