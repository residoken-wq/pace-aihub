---
trigger: glob
globs: apps/api/app/gateway/**, apps/worker/**/ai/**, packages/contracts/schemas/**
---
# Claude Gateway & AI output rules

- Single entry point: `gateway.analyze(evidence_refs, policy, schema, run_ctx) -> (report_json, usage)`.
- Order: authorize → check tool published + allowed model → estimate cost from `model_price_versions` (effective-dated, never hard-coded prices) → reserve → call Anthropic Messages API (timeout, correlation id) → settle/release → ledger.
- `spent + reserved + requested > hard_limit` → `429 BUDGET_EXCEEDED`. Never fall back to another team's pool/key.
- Model output must validate against `packages/contracts/schemas/daily_brief.schema.json`. One bounded repair attempt; else run → `needs_review` / `MODEL_RESPONSE_INVALID`. Never auto-send.
- DailyBrief rules: groups customer/competitor/market, ≤5 items each, every fact has `source_ids` that exist in this run, label [Sự kiện] vs [Suy luận], empty group = "Không có cập nhật đáng kể", Vietnamese, email ≤500 words.
- Tests use recorded/mocked provider responses; no real API calls in CI. Include fixtures with prompt-injection text and fabricated URLs that must be rejected.
