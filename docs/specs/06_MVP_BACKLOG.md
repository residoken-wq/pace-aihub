# 06 — MVP Backlog & Delivery Plan
**Estimates:** ideal developer-days, directional only; dependencies and acceptance required before commitment. Suggested team: 1 FE, 1 BE, 0.5 DevOps/Security, 0.5 QA/PO.

> **Bổ sung theo ADR-014 (20/10/2026):** thêm UI-00 và CMS-01 vào P0 — xem cuối bảng. Kế hoạch phase hiện hành: `docs/plan/PHASES.md`.

| ID | Epic / Story | Priority | Est. dev-days | Depends on | Definition of Done |
|---|---|---|---:|---|---|
| P0-01 | Verify Anthropic API entitlement, price, billing and credit | P0 | 2 | Owner access | Written Console evidence, budget cap |
| P0-02 | Verify Graph/Power Automate licensing and consent | P0 | 2 | Tenant admin | Permissions matrix approved |
| P0-03 | Data classification & privacy threat model | P0 | 3 | Data owners | DLP/retention approval |
| INF-01 | Docker, CI/CD, secrets, TLS, backups | P0 | 6 | P0 | Restore test passed |
| AUTH-01 | Entra SSO, session, workspace RBAC | P0 | 7 | P0 | IDOR tests pass |
| DB-01 | Migrations, constraints, tenant-safe repositories | P0 | 5 | AUTH | Schema & migration test |
| TOOL-01 | Template catalog, draft/version/publish | P0 | 7 | AUTH/DB | Clone + publish workflow |
| UI-01 | Dashboard and Sales wizard | P0 | 8 | TOOL | Usability test 5 users |
| COL-01 | RSS collector, canonical URL, dedupe | P0 | 6 | DB | Fixture tests and retry |
| COL-02 | Outlook Google Alerts adapter | P0 | 6 | P0-02 | Scoped mailbox consent + fixture |
| RUN-01 | Scheduler, durable queue, idempotency | P0 | 8 | INF/DB | No duplicate schedule run |
| GW-01 | Vault-backed Claude Gateway + model policies | P0 | 7 | P0-01 | No exposed keys |
| GW-02 | Quota reservation, ledger, reconciliation | P0 | 9 | GW/DB | Concurrent budget test |
| AI-01 | Sales analysis schema, provenance, validation | P0 | 8 | COL/GW | Invalid citations rejected |
| RPT-01 | Preview, approve/reject, revision | P0 | 6 | AI/AUTH | Only reviewer approves |
| OUT-01 | Outlook dispatch + audit + idempotency | P0 | 5 | P0-02/RPT | Duplicate email prevented |
| OBS-01 | Run history, failures, audit, alerts | P0 | 6 | RUN | Operational runbook |
| QA-01 | Security, integration, UAT, load tests | P0 | 10 | all | Exit gates met |
| UI-00 | Design system, AppShell, StatusBadge, 5-state patterns (ADR-014) | P0 | 3 | — | Tokens applied, a11y check |
| CMS-01 | Admin console (Team Mgmt, Credentials refs, Policies, Audit) + Budget dashboard (ADR-014) | P0 | 6 | AUTH/GW-02 | Admin-only enforced server-side |
| SP-01 | SharePoint archive + document link | P1 | 5 | P0-02 | Team ACL verified |
| AI-02 | Weekly Review + Action Plan | P1 | 7 | AI-01 | Only approved evidence |
| COL-03 | Outlook Calendar reminders | P1 | 5 | P0-02 | Delegated scope tested |
| UX-02 | Marketplace search + template-only sharing | P1 | 5 | TOOL | No data leaks |

**Total directional P0 effort:** ~105 developer-days (≈114 sau ADR-014), parallelizable but subject to integration uncertainty. 2–3 week implementation is not a credible commitment for this scope without substantial reuse or reduced scope. Start with a vertical slice first.

## Suggested releases
- **Gate 0 / Week 1–2:** P0-01..03; go/no-go; acceptance of legal/licensing and source policy.
- **Slice 1 / Weeks 3–5:** Entra, workspace, one Sales template, RSS ingest, manual run, Claude Gateway, preview (no email automation).
- **Slice 2 / Weeks 6–8:** budget hard caps, scheduler, Google Alerts mailbox, approvals, Outlook dispatch, audit.
- **Pilot / Weeks 9–11:** Sales users, then IT; security tests, runbooks, backups, quota tuning.
Timelines are planning hypotheses for staffed delivery, not vendor commitments. (Superseded by `docs/plan/PHASES.md`.)

## UAT scenarios
UAT-01 create Sales tool in <10 minutes; UAT-02 duplicate URL skipped; UAT-03 Monday lookback correct; UAT-04 no source = explicit no updates; UAT-05 3 categories <=5 items; UAT-06 report has source links and [Sự kiện]/[Suy luận]; UAT-07 report approval before email; UAT-08 team user forbidden to other team's report; UAT-09 exhausted budget blocks run; UAT-10 retry doesn't duplicate email; UAT-11 revoke member blocks access; UAT-12 usage matches ledger.

## Release gate
GO only when: approved permissions; validated credit/billing; zero high/critical vulnerabilities; no leaked keys; cross-team authorization tests pass; >95% scheduled success over 30+ trial runs; source attribution validated; data owners sign off.
