# 07 — Architecture Decisions, Open Questions, Test Strategy

## ADRs proposed
| ADR | Decision | Rationale | Revisit trigger |
|---|---|---|---|
| ADR-001 | Native template-driven builder, not arbitrary visual workflow engine | Safer, faster MVP | >20 workflow types |
| ADR-002 | Claude API behind shared gateway | Quotas, no shared secrets | Provider strategy changes |
| ADR-003 | Entra SSO + workspace RBAC | Existing Microsoft tenant | External users |
| ADR-004 | PostgreSQL metadata + SharePoint documents | Relational audit and organizational storage | Data residency requirement |
| ADR-005 | Power Automate only where standard connectors fit | Avoid hidden Premium costs | Enterprise license change |
| ADR-006 | Approval before distribution by default | Sales data and hallucination risk | Data owners approve auto-send |
| ADR-007 | Source allowlist and fixed connector set | Prevent SSRF/exfiltration | Connector security framework |
| ADR-008 | Monthly hard cap and per-run reservation | Avoid runaway spend | Billing reconciliation proves alternative |

## Questions requiring signoff
- Anthropic Console organization and API credits: actual amount, expiry, eligibility, pricing, spend limits? **Unverified.**
- Which team owns provider API key and invoice? What happens when credit expires?
- Can IT obtain Graph permissions for a dedicated mailbox/SharePoint site without broad tenant access?
- Which Sales sources and competitors are authorized? Are personal/customer emails allowed in model inputs?
- Is content confidential or personal data? Which geographic/data processing rules apply?
- Number of users, teams, daily runs, maximum monthly spend, support ownership?
- Required availability, backup, retention and approval roles?

## Phase 0 evidence checklist
- [ ] Screenshot/export from Anthropic Console billing + API usage entitlement (no secret values).
- [ ] Graph permissions matrix, admin consent record, Power Automate license review.
- [ ] Sample 20 Google Alerts/RSS messages anonymized, Sales validates relevance.
- [ ] Source/data classification, PII handling, retention approved.
- [ ] Run one end-to-end prototype with real Claude API and measured usage.
- [ ] BOD accepts budget cap, owners and scope.

## Test matrix
**Security:** OIDC validation, CSRF, SSRF DNS rebinding, injection in RSS/email, secret exfiltration, workspace IDOR, recipient spoofing, excessive scopes, SQLi, log redaction.
**Reliability:** 429/5xx retry, worker crash, queue replay, schedule overlap, quota race, model malformed JSON, source 404, Graph 401/403, email duplicate.
**Quality:** source attribution, no fabricated URLs, empty category, Monday window, 5/category limit, Vietnamese quality, report versioning.
**Operational:** backup restore, key rotation, revoke user, audit export, retention purge, budget 80% warning / 100% deny.

## Definition of done for implementation handoff
PRD approved; ADRs accepted; source and data policies approved; secrets plan reviewed; SQL migrations tested; OpenAPI contract produced; prototype usability validated; backlog sized by actual team; BOD release gate documented.
