# 05 — UI/UX Specification & Clickable Prototype

## Product navigation
Left sidebar: Home, My Tools, Team Tools, Templates, Runs & Reports, Knowledge, Usage & Budget, Settings. Admin-only: Team Management, Credentials (references only), Policies, Audit.

## Screens
| Screen | Primary action | Important states |
|---|---|---|
| Dashboard | Open/create tool | Empty, loading, quota warning, errors |
| Template catalog | Choose Sales Intelligence | Search, category, details |
| Create tool wizard | 1 Scope → 2 Sources → 3 AI Instructions → 4 Schedule & Output → 5 Preview & Publish | Validation, permissions, unsaved draft |
| Tool detail | Run now, schedule, clone, share | Draft, published, paused, archived |
| Run history | Filter status, inspect evidence | Queued/running/partial/failed/success |
| Report review | Facts vs Inferences, approve/reject | Pending/approved/rejected/sent |
| Budget dashboard | Usage by team/tool, quota | 80% warning, 100% blocked |
| Admin console | Membership, allowlist, provider secret reference | Permission denied, rotate |

## Sales Wizard — exact fields
1. **Scope:** Personal/Team; owner team; title; template version.
2. **Sources:** RSS URLs allowlisted; Google Alerts via authorized shared Outlook mailbox/folder; market keywords; customer list; competitor list; optional calendar scope. Show source verification status.
3. **AI Policy:** language Vietnamese; max 5 items/group; label [Sự kiện]/[Suy luận]; source required; no filler; prompt preview (system policy locked).
4. **Schedule:** IANA timezone Asia/Ho_Chi_Minh; time 08:30; weekdays; Monday lookback Friday 08:00; email recipients approved; archive location.
5. **Preview:** estimated budget, dry run, report evidence, request publish approval.

## Key interaction rules
- Button 'Run now' returns a real queued run in production; prototype only demonstrates local UI and does not call APIs.
- 'Share tool' requires team membership and only shares template/config permitted by policy; sources and reports remain separately authorized.
- Warn before enabling auto-dispatch; default is reviewer approval.
- A failed source shows partial report banner; never label complete.
- Show 'Estimated cost' and 'Actual cost' separately, and remaining hard cap.
- Date and times displayed local with timezone label; store UTC.
- WCAG 2.2 AA goal: contrast, keyboard focus, labeled inputs, error messages, mobile responsive.

## Prototype
Open [prototype.html](prototype.html) in a browser. Screens: dashboard, wizard, runs, budget. Mock data only; interactions are client-side and do not persist to backend. No real secret entry field is provided by design.

## Suggested design system
Primary blue #1E88E5, orange accent #FB8C00, neutral gray; Roboto/system font; 8px spacing, 12px cards; readable desktop 1440px and mobile 390px; explicit status icons + text, not color only.
