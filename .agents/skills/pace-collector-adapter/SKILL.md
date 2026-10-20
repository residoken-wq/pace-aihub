---
name: pace-collector-adapter
description: Build or change a PACE AI Hub source collector (RSS feed, Google Alerts via authorized Outlook mailbox/folder, Outlook Calendar) including normalization, canonical URL, dedupe, time window and SSRF protection. Use for COL-01, COL-02, COL-03 or any ingestion code.
---
# Collector adapter

Contract: `collect(config, cursor) -> list[NormalizedItem]` (+ new cursor, per-source errors).

1. **Fetch safely** (`app/collectors/http.py` shared client): host allowlist from workspace policy; resolve DNS and reject private/link-local/metadata IPs, re-validate on redirect; timeout 10s; max 2 MB; accept only rss/atom/xml/html types; user-agent identifies PACE.
2. **Outlook/Google Alerts:** Microsoft Graph with the approved scope only (dedicated mailbox/folder; no tenant-wide read). Extract target URLs from Google redirect links (`url=` / `q=` param). Treat email HTML as untrusted; strip scripts; keep minimal text.
3. **Normalize:** `title, canonical_url, published_at (UTC), source_kind, snippet (≤ 1,000 chars), metadata`. Canonical URL: lowercase host, remove fragments and tracking params (`utm_*`, `gclid`, `fbclid`, `ved`, `usg`), resolve Google redirect, strip default ports.
4. **Dedupe:** `url_hash = sha256(canonical_url)`, `content_hash = sha256(normalized title+snippet)`; upsert on `(workspace_id, url_hash)`; similar-but-different URLs → keep both, flag for review (do not merge automatically).
5. **Window:** rolling 24h; Monday from Friday 08:00 local (configurable), using IANA tz.
6. **Partial failure:** one failing source must not fail the run; record error per source; report shows "chưa đầy đủ".
7. **PII:** redact emails/phones in snippets before AI analysis.
8. **Tests:** fixture feeds in `tests/fixtures/sources/` (20 samples: duplicates, tracking params, Google redirect, malformed XML, 404, huge payload, private-IP redirect, injection text). Freeze time for Monday window tests (UAT-02, UAT-03, UAT-04).
