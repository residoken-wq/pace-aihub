---
name: pace-ui-screen
description: Build or modify a PACE AI Hub screen (CMS/admin console or end-user UI) — dashboard, list/table, detail, multi-step wizard, report review, budget dashboard, admin pages. Use for any page, layout, form or UI flow work in apps/web.
---
# Build a PACE screen

## 1. Spec first
- Find the screen in `docs/specs/05_UI_UX_SPEC.md` (primary action, states, exact wizard fields). Open `docs/specs/prototype.html` for layout intent only (mock data, not production code).
- Write a 5-line screen brief: user/persona, primary job, data needed (endpoint), actions + permissions, states.

## 2. Pick the page pattern (`components/patterns/`)
| Pattern | Use for | Must include |
|---|---|---|
| `AppShell` | all pages | sidebar (role-aware), top bar with workspace switcher (Personal/Team), breadcrumb, user menu |
| `ListPage` | My Tools, Team Tools, Runs, Audit | search, filters (status chips), sortable table, pagination, empty state CTA, row actions menu |
| `DetailPage` | Tool detail, Run detail | header (title + StatusBadge + primary action), tabs (Overview / Versions / Runs / Settings), side panel metadata |
| `WizardPage` | Create tool (5 steps) | stepper, per-step zod validation, autosave draft, "unsaved changes" guard, back/next, final review |
| `ReviewPage` | Report review | 2-column: report (facts vs inferences) / evidence panel (sources, URLs, published_at); approve/reject with reason; revision history |
| `DashboardPage` | Home, Usage & Budget | KPI cards, budget meter, charts (Recharts), recent runs, alerts |
| `SettingsPage` | Admin: members, allowlist, credentials refs, policies | forms in cards, destructive zone, confirm dialogs, audit note |

## 3. Implement
- Server Component page fetches with generated client; client islands for interactivity. TanStack Query for mutations + polling of run status (aria-live).
- Implement all 5 states (loading skeleton, empty, error + retry + request_id, partial/warning banner, success).
- Permission-aware UI: hide/disable actions the role can't do, with tooltip reason; never rely on UI hiding for security.
- Vietnamese copy via i18n keys; dates `08:30 (GMT+7)`; money `$12.34` with 2 decimals display.
- Specific rules: Run now → toast with run link; Share tool → dialog explaining tool ≠ data ≠ credential sharing; enabling auto-dispatch → warning confirm; failed source → "Báo cáo chưa đầy đủ" banner; show Estimated vs Actual cost + remaining cap.

## 4. Verify
- Component tests for states; Playwright test for the main flow (tag UAT ID).
- Use the browser agent: screenshot 1440px & 390px, tab through the page, check focus ring and contrast. Fix before reporting.
- Run `/pace-ux-review` on the screen for a heuristic pass.
