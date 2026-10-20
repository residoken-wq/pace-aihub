---
name: pace-phase-gate
description: Run the exit-gate review for a PACE AI Hub phase (Phase 0–6) — check scope completed, exit criteria, test/UAT evidence, security verdict, open risks — and produce a GO / NO-GO report for the BA/PM and BOD. Use when the user asks "phase review", "gate", "are we ready", "release readiness".
---
# Phase gate review

1. Read `docs/plan/PHASES.md` for the phase scope and exit criteria; read `docs/traceability.md`.
2. For each story in scope: status, tests, UAT IDs, open defects. Mark DONE / PARTIAL / NOT STARTED with evidence.
3. Run full suite (`pytest`, web unit, Playwright e2e) and summarize pass/fail counts.
4. Run `/pace-security-review` on the phase diff (`git diff <phase-start-tag>..HEAD`).
5. Check phase-specific metrics (e.g. Phase 5: ≥30 runs, ≥95% scheduled success, ≥90% claims with verifiable URL, zero cross-team reads, cost ≤ budget, Sales ≥4/5 on ≥20 briefs).
6. Write `docs/plan/gate-reports/phase-<n>-<yyyymmdd>.md`:
   - Verdict: GO / GO with conditions / NO-GO
   - Exit criteria table (criterion | evidence | met?)
   - Defects (severity), risks (RAID), decisions needed (owner)
   - Scope moved to next phase
7. Never mark GO if a Critical/High security finding or failing required test exists.
