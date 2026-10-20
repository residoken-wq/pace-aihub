---
trigger: always_on
---
# Security baseline (PACE AI Hub)

- AuthN: Entra ID OIDC, authorization code + PKCE, server-side session in HttpOnly Secure SameSite cookie; CSRF token on state-changing requests.
- AuthZ: resolve `workspace_id` from the resource in the DB (never trust client-supplied workspace for authorization); check membership + role (`viewer < member < editor < admin`). Return `403 WORKSPACE_FORBIDDEN` (or 404 for existence hiding where specified).
- Every repository query on tenant data filters by `workspace_id`. Add a test proving user of team A cannot read/modify team B's resource.
- Secrets: only via settings loaded from env/vault (`pydantic-settings`, `SecretStr`). Never log, echo, serialize or put in fixtures. Credentials API stores `vault_ref` + fingerprint only.
- Logging: structured JSON; redact `Authorization`, cookies, tokens, email bodies, source text, PII.
- Outbound fetch (collectors): allowlisted hosts only; block RFC1918, link-local, metadata IPs; re-check after DNS resolution (rebinding); timeouts; max bytes; content-type check.
- Prompt injection: system policy is code-owned and versioned; source text wrapped as data; model output validated against JSON Schema; citations must resolve to collected `source_item` IDs; no model-initiated tool calls or URLs.
- Never auto-send. Dispatch requires `report.status = approved` and recipient in approved allowlist.
- Write an `audit_events` row for: publish, approve/reject, dispatch, credential ops, membership changes, budget changes.
- Public repo (ADR-015): before every commit, check the diff for internal hostnames/IPs, tenant IDs, real business data; move them to gitignored paths. If a secret was ever committed, tell the user to rotate it — deleting the commit is not enough.
- Do not disable TLS verification, CSRF, or auth in code, even "temporarily for dev".
