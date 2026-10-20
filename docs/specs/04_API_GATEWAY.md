# 04 — Claude API Gateway & Shared Credits Governance

## Principle
**Share spending capacity, never share the key.** Claude Team Standard chat subscription does not automatically grant usable Claude API credit. Confirm Anthropic Console organization, billing, any promotional entitlement, model pricing, spend limits and rate limits before Phase 1. Never use chat session cookies/tokens as API credentials.

## Key hierarchy
- `provider_account` (Anthropic Console org) → `credential_ref` in secret vault → `budget_pool` (Org/Team/Personal) → `budget_allocation` → `tool` → `run`.
- Team admins may request/use approved pool, cannot read raw secret. IT rotates/revokes.
- Optional BYOK **post-MVP** only after policy/security review, key ownership and revocation support.

## Budget controls
1. Platform Admin defines monthly hard cap in USD (internal), team cap, tool cap, per-run max input/output tokens, max concurrent requests, rate limits.
2. At inference: validate membership, tool published, data classification, allowed model, recipient policy.
3. Calculate conservative estimated charge from model price snapshot + max tokens (or enforce preflight prompt token count); reserve quota transactionally before calling provider.
4. Call provider with timeout, idempotency/run correlation; log usage tokens from provider response.
5. Reconcile reservation to actual charge, release unused amount; stale reservations swept by reconciliation job.
6. If provider billing actual differs (cache reads, tools, pricing changes), ledger records adjustments with reference; reconcile daily with Console usage/billing export if available.
7. `spent + reserved + requested > hard_limit` → HTTP 429 `BUDGET_EXCEEDED`; soft 80% alert; no auto-overage.
8. Credit grants, if any, tracked separately from cost; never treat seat count as guaranteed credits.

## Cost model
`estimated_cost_usd = input_tokens * input_price_per_million / 1e6 + output_tokens * output_price_per_million / 1e6 + other_provider_charges`. Model prices in `model_price_versions` effective-dated; no hardcoded unverified current rates. Ledger stores estimated, provider reported, settled, currency, and price version. Decimal numeric, not float.

## Internal API v1 (illustrative)
- `POST /api/v1/tools` create draft (workspace membership).
- `POST /api/v1/tools/{id}/publish` team admin approval.
- `POST /api/v1/tools/{id}/runs` manual execution; returns `202 {run_id,status}`.
- `GET /api/v1/runs/{id}` status, sources, report, cost (scoped).
- `POST /api/v1/reports/{id}/approve` reviewer only.
- `POST /api/v1/reports/{id}/dispatch` idempotent, approved only.
- `GET /api/v1/budgets/{pool_id}/usage?month=YYYY-MM`.
- `POST /api/v1/admin/credentials` registers vault reference, never echoes key.

### Sample request
```json
{
  "tool_version_id": "UUID",
  "mode": "preview",
  "idempotency_key": "user-supplied-uuid"
}
```
### Sample response
```json
{"run_id":"UUID","status":"queued","budget_reservation_id":"UUID"}
```
### Errors
`401 UNAUTHENTICATED`, `403 WORKSPACE_FORBIDDEN`, `409 DUPLICATE_RUN`, `422 INVALID_SOURCE_CONFIG`, `429 BUDGET_EXCEEDED`, `429 PROVIDER_RATE_LIMIT`, `502 MODEL_RESPONSE_INVALID`, `503 CONNECTOR_UNAVAILABLE`.

## Concurrency & transactional correctness
- Use PostgreSQL transaction with `SELECT ... FOR UPDATE` on budget allocation row; calculate `spent + reserved`; create unique reservation by run/request key; commit **before** provider call.
- Worker retry must reuse run ID and avoid double billing/reservation; provider may charge for ambiguous timeouts, record uncertain status and reconcile rather than blindly retry indefinitely.
- Finalization in transaction: decrement reserved, increment spent, write append-only usage ledger; avoid negative balances. Monthly boundaries based on UTC or explicit configured billing timezone (pick one and document).
- Provider workspace spending limits are second independent safety boundary; internal limits alone are insufficient.

## Security & privacy
- Secrets vault with KMS; rotation, access logs; redact Authorization headers, source text and PII from request logs.
- Restrict tool prompt to system-owned policy + versioned template; user input treated as data; output schema validation; citations must resolve to collected source IDs.
- For prompt injection: never follow instructions in articles/email; no model-initiated outbound calls or arbitrary tool invocation.
- Tenant separation enforced in SQL/API; test IDOR and privilege escalation; enforce team-level row filters; no user-created provider URLs.

## Minimum gateway tests
1. Concurrent 20 requests at remaining budget $1: accepted reservations never exceed $1.
2. Non-member cannot spend from team pool.
3. Key never appears in API response/browser/network log.
4. Crash after reservation → TTL reconciliation releases/flags accurately.
5. 429 provider and timeouts obey bounded retry and spend guard.
6. Cross-team prompt data not visible via report or logs.
7. Price update preserves historical ledger calculation.
8. Report dispatch rejects unapproved report.
