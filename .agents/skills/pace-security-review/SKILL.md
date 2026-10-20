---
name: pace-security-review
description: Security review of PACE AI Hub code changes or a phase release — auth, workspace authorization (IDOR), secrets, SSRF, prompt injection, budget abuse, logging, dependencies. Use before merging auth/gateway/collector/dispatch code and at every phase exit gate.
---
# Security review

Output: findings table `ID | Severity (Critical/High/Medium/Low) | File:line | Issue | Exploit scenario | Fix`, then a verdict (PASS / PASS with conditions / FAIL). Any Critical/High = FAIL.

## Checks
1. **AuthN/session:** OIDC state/nonce/PKCE validated; cookie flags; session revoked on offboarding (UAT-11); CSRF on POST/PUT/PATCH/DELETE.
2. **AuthZ:** each new route has role dependency; repository queries filter `workspace_id`; IDs from path verified against user membership; admin routes double-checked; write a failing test if missing.
3. **Secrets:** grep diff for keys/tokens (`sk-ant-`, `Bearer`, `client_secret`); run `gitleaks`; settings use `SecretStr`; no secrets in `NEXT_PUBLIC_*`, fixtures, logs, error messages.
4. **SSRF:** collectors use shared safe client; redirects re-validated; private IP blocked.
5. **Injection:** SQL only via ORM/bound params; HTML from sources sanitized before render (no `dangerouslySetInnerHTML` without sanitizer); prompt-injection fixtures pass; model output never executed or used as URL to fetch.
6. **Money/budget:** reservation before call; no float; no path to bypass gateway; concurrency test present.
7. **Dispatch:** approved-only; recipient allowlist; idempotency key; no customer auto-email.
8. **Logging/audit:** redaction; audit events for sensitive ops.
9. **Dependencies:** `pnpm audit --prod`, `uv pip audit`/`pip-audit`, container scan (`trivy`) at phase gates.
