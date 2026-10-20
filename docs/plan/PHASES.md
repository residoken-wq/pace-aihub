# PACE AI Hub — Phase Plan (v1.3, 20/10/2026)
> **Changelog v1.3:**
> - Kickoff 20/10/2026, quy đổi W1–W15 sang lịch thật.
> - Thêm lịch nghỉ Tết 2027 vào kế hoạch.
> - ADR-015: repo tạm thời public, hạn xem lại 30/10/2026.
> **Changelog v1.2:**
> - IT bàn giao VM trong 48h sau kickoff, nên deploy walking skeleton ngay ở Phase 1.
> - Bật bắt buộc secret scanning + push protection.
> - ADR-014 đưa CMS-01 và UI-00 vào P0.
> - Chủ dự án là approver duy nhất, kèm SLA và ủy quyền.
> **Changelog v1.1:** chốt ADR-009 (GitHub Actions + GHCR), ADR-010 (pilot trên VM nội bộ, deploy pull-based), ADR-011 (đội 4 người), ADR-012 (cho phép Antigravity). Thêm việc hạ tầng VM vào Phase 0/1/4, thêm skill `pace-deploy-vm`, ước lượng CMS-01/UI-00, kiểm tra năng lực đội.

> Kế hoạch là **giả thuyết lập kế hoạch**, không phải cam kết. Ước lượng gốc P0 ≈ 105 dev-days (06_MVP_BACKLOG). Đội: **4 người** (ADR-011): Tech Lead/BE, FE/UI, Fullstack/DevOps-Sec, BA-PO/QA Lead, cộng thêm Antigravity agent. AI agent rút ngắn thời gian viết code nhưng **không** rút ngắn các gate về license, bảo mật, dữ liệu và UAT.
> Mốc tuần tính từ ngày kickoff (W1). Mỗi phase kết thúc bằng `/pace-phase-gate`.

## Tổng quan
**Kickoff: thứ Ba 20/10/2026.** Tuần tính từ thứ Hai đến thứ Sáu. IT bàn giao VM trước **22/10/2026**.


| Phase | Tuần | Mục tiêu | Story chính | Kết quả demo |
|---|---|---|---|---|
| 0 — Gate 0: Discovery & Setup | W1–W2 | Xác minh license/credit/quyền, chuẩn bị repo + Antigravity | P0-01, P0-02, P0-03 | Evidence pack + repo có specs, rules, skills |
| 1 — Foundation | W2–W4 | Nền móng chạy được: repo, CI, SSO, workspace RBAC, DB, design system, AppShell | INF-01 (phần dev/CI), AUTH-01, DB-01 | Đăng nhập Entra → chọn Personal/Team workspace → shell UI |
| 2 — Vertical Slice 1 | W5–W7 | Tạo Sales tool từ template → chạy tay với RSS → xem brief có nguồn | TOOL-01, UI-01, COL-01, GW-01, AI-01, RUN-01 (manual), RPT-01 (preview) | Brief thật từ Claude API, không gửi email |
| 3 — Slice 2: Governance & Automation | W8–W10 | Ngân sách cứng, lịch chạy, Google Alerts, duyệt, gửi Outlook, audit, CMS admin | GW-02, RUN-01 (scheduler), COL-02, RPT-01 (approve/revision), OUT-01, OBS-01 | Lịch 08:30 chạy → duyệt → gửi mail idempotent; budget 80/100% |
| 4 — Hardening & QA | W11–W12 | Bảo mật, độ tin cậy, vận hành, UAT dry-run | QA-01, INF-01 (TLS, backup/restore, secrets) | Release candidate, security verdict PASS |
| 5 — Pilot | W13–W15 | Sales → IT dùng thật, đo KPI, BOD GO/NO-GO | Vận hành, tuning quota, fix defects | Gate report cho BOD |
| 6 — P1 Enhancements | Sau GO | Lưu trữ SharePoint, Weekly/Action Plan, Calendar, Marketplace, template phòng ban thứ 2 | SP-01, AI-02, COL-03, UX-02 | Mở rộng nền tảng |

## Lịch thực tế
| Phase | Tuần | Từ | Đến | Mốc chính |
|---|---|---|---|---|
| 0 | W1–W2 | 20/10/2026 | 30/10/2026 | 22/10: nhận VM · 30/10: Gate 0 + xem lại ADR-015 (public repo) |
| 1 | W2–W4 | 26/10/2026 | 13/11/2026 | 13/11: walking skeleton trên VM, SSO, RBAC |
| 2 | W5–W7 | 16/11/2026 | 04/12/2026 | 04/12: demo Slice 1 (brief thật từ RSS) |
| 3 | W8–W10 | 07/12/2026 | 25/12/2026 | 25/12: demo Slice 2 (lịch, duyệt, gửi mail, budget) |
| 4 | W11–W12 | 28/12/2026 | 08/01/2027 | 01/01/2027 nghỉ Tết Dương lịch (mất 1 ngày) · 08/01: release candidate |
| 5 | W13–W15 | 11/01/2027 | 29/01/2027 | 29/01: gate report GO/NO-GO |
| — | W16 | 01/02/2027 | 03/02/2027 | BOD quyết định trước Tết; dự phòng |
| Nghỉ Tết | — | 04/02/2027 | 10/02/2027 | Dự kiến theo nguồn báo chí; lịch chính thức chưa công bố |
| 6 | Sau Tết | từ 15/02/2027 | — | P1 enhancements nếu GO |

**Lưu ý lịch:**
- Pilot (11–29/01) rơi vào giai đoạn cận Tết, khi Sales bận chốt cuối năm. Nên chốt danh sách người dùng pilot và mục tiêu ≥20 brief được chấm điểm ngay từ Phase 3.
- Tuần cuối tháng 12 dễ thiếu người vì nghỉ lễ; việc của Phase 3–4 cần lịch nghỉ của đội sớm.
- Không có buffer sau W16: nếu trễ hơn 1 tuần, GO/NO-GO sẽ lùi sang sau Tết (≈ 15/02/2027).

---

## Phase 0 — Gate 0: Discovery & Setup (W1–W2)
**Mục tiêu:** chỉ commit MVP khi có bằng chứng. Song song chuẩn bị môi trường coding.
- **Business/IT (không phải agent):**
  - P0-01: bằng chứng Anthropic Console (org, billing, credit, giá model, spend limit, rate limit). Claude Team ≠ API miễn phí.
  - P0-02: ma trận quyền Graph (mailbox chuyên dụng, Sites.Selected), Power Automate license (standard vs premium), admin consent.
  - P0-03: phân loại dữ liệu, PII, retention (90d/365d đề xuất), DLP.
  - Thu 20 mẫu Google Alerts/RSS đã ẩn danh; Sales xác nhận độ liên quan.
  - **Hạ tầng (ADR-010), IT bàn giao trong 48h sau kickoff:**
    - Cấp VM nội bộ riêng (Ubuntu 24.04; đề xuất 4 vCPU/16 GB/100 GB, là giả định).
    - Domain nội bộ + chứng chỉ TLS.
    - Firewall egress allowlist: `api.anthropic.com`, `login.microsoftonline.com`, `graph.microsoft.com`, `ghcr.io`, các host RSS đã duyệt.
    - Nơi lưu backup ngoài VM.
    - Entra app registration (dev + pilot) với redirect URI nội bộ.
  - **GitHub (ADR-009):**
    - Repo private, branch protection, Environments `dev`/`pilot`.
    - GHCR private; **secret scanning + push protection bắt buộc** (đã xác nhận có).
  - Scheduler: Celery beat trên VM là mặc định. Power Automate chỉ dùng cho flow chạy được bằng standard connector.
- **Antigravity setup:** xem `SETUP.md` — đưa specs vào `docs/specs/`, cài rules + skills, cấu hình bảo mật agent, cài skill bên thứ ba đã audit.
- **Agent được phép làm:** spike kỹ thuật không cần credential thật (ví dụ: chạy thử Claude API bằng key sandbox do IT cấp với hạn mức nhỏ → đo token thật cho 1 brief).
- **Exit criteria:**
  - Phase 0 checklist trong `07` hoàn thành ≥ 5/6.
  - BOD chấp nhận budget cap và owner.
  - ADR-013 tech stack được chốt.
  - Repo có AGENTS.md, rules, skills và CI skeleton xanh.
  - VM đã được bàn giao (≤48h sau kickoff), SSH bằng tài khoản deploy, kiểm tra egress đạt.
- **Rủi ro:**
  - Credit không như kỳ vọng → điều chỉnh ngân sách.
  - Graph scope bị từ chối → chuyển sang chỉ dùng RSS cho Slice 1.
  - Cấp VM chậm (rủi ro **Thấp** nhờ cam kết 48h) → dev và CI vẫn chạy bình thường; chỉ chặn việc deploy.

## Phase 1 — Foundation (W2–W4)
| Story | Nội dung | Skill Antigravity |
|---|---|---|
| INF-01a | Monorepo, docker-compose dev, GitHub Actions `ci.yml` + `build.yml` (GHCR), pre-commit, Dependabot | `pace-repo-bootstrap` |
| DB-01 | Alembic baseline từ `03_DATABASE_SCHEMA.sql`, repository workspace-scoped, seed dev | `pace-db-migration` |
| AUTH-01 | Entra OIDC + PKCE, session cookie, CSRF, workspace membership/roles, offboarding revoke | `pace-fastapi-endpoint`, `pace-security-review` |
| INF-01c | **Walking skeleton lên VM:** `compose.prod.yml` tối thiểu + deploy pull-based từ GHCR + TLS + `/healthz`. Sau đó mỗi lần merge `main` có thể deploy bản mới lên VM | `pace-deploy-vm` |
| UI-00 | Design tokens, shadcn primitives, AppShell (sidebar role-aware, workspace switcher), i18n vi, StatusBadge, 5-state patterns | `pace-design-system`, `pace-ui-screen` |
- **Exit:** walking skeleton chạy trên VM nội bộ qua HTTPS; login SSO thật (tenant dev); non-member nhận 403 (FR-01); IDOR test suite pass; CI xanh; migration up/down pass; AppShell đạt a11y check.
- **Demo:** đăng nhập → thấy Personal + Team workspace → điều hướng các menu rỗng (empty states).

## Phase 2 — Vertical Slice 1 (W5–W7)
| Story | Nội dung | Skill |
|---|---|---|
| TOOL-01 | Template catalog, tool draft/version/publish (immutable version, rollback) | `pace-fastapi-endpoint`, `pace-db-migration` |
| UI-01 | Dashboard, Template catalog, Wizard 5 bước (Scope → Sources → AI Policy → Schedule & Output → Preview), Tool detail | `pace-ui-screen`, `pace-ux-review` |
| COL-01 | RSS collector, safe HTTP client (SSRF), canonical URL, dedupe, time window | `pace-collector-adapter` |
| GW-01 | Gateway: vault/env key, model policy, price versions, provider call, usage log (reservation đơn giản) | `pace-claude-gateway` |
| AI-01 | Prompt policy Sales v1, DailyBrief JSON schema, validation citation, repair 1 lần | `pace-claude-gateway`, `pace-qa-testcases` |
| RUN-01a | Manual run: `POST /tools/{id}/runs` → 202, worker pipeline, run status polling | `pace-fastapi-endpoint` |
| RPT-01a | Report preview: Facts vs Inferences + evidence panel | `pace-ui-screen` |
- **Exit:** UAT-01 (≤10 phút), UAT-02, UAT-04, UAT-05, UAT-06 pass; key không xuất hiện ở browser/log; golden set 20 bundle chạy được, schema pass 100%.
- **Demo:** Sales tạo tool, bấm "Chạy ngay", xem brief tiếng Việt có link nguồn.

## Phase 3 — Slice 2: Governance & Automation (W8–W10)
| Story | Nội dung | Skill |
|---|---|---|
| GW-02 | Reservation atomic (FOR UPDATE), settlement, ledger, reconciliation job, 80/100% alert | `pace-claude-gateway` |
| RUN-01b | Scheduler (Celery beat), unique schedule slot, Monday lookback, retry/backoff, DLQ | `pace-fastapi-endpoint`, `pace-qa-testcases` |
| COL-02 | Google Alerts qua mailbox/folder Outlook được cấp quyền (Graph) | `pace-collector-adapter` |
| RPT-01b | Approve/reject (lý do), regenerate = revision mới, chỉ reviewer duyệt | `pace-ui-screen`, `pace-fastapi-endpoint` |
| OUT-01 | Outlook dispatch idempotent, recipient allowlist, audit | `pace-fastapi-endpoint`, `pace-security-review` |
| OBS-01 | Run history, failure detail, audit log, metrics, alerts | `pace-ui-screen` |
| CMS-01 | Admin console: Team Management, Credentials (chỉ vault ref), Policies (source allowlist, models, recipients), Audit viewer, Budget dashboard | `pace-ui-screen`, `pace-ux-review` |
- **Exit:** UAT-03, 07, 08, 09, 10, 11, 12 pass; test 20 request đồng thời ≤ $1; không có scheduled run trùng; dispatch chỉ khi approved.
- **Demo:** 08:30 tool tự chạy → reviewer duyệt → email gửi 1 lần; team hết budget bị chặn với thông báo rõ.

## Phase 4 — Hardening & QA (W11–W12)
- QA-01: full test matrix (security, reliability, quality, operational) từ `07`; load test nhẹ (số team × run/ngày dự kiến); DAST cơ bản (OWASP ZAP baseline).
- INF-01b, trên **VM nội bộ** (ADR-010):
  - `compose.prod.yml`, deploy/rollback kiểu pull từ GHCR.
  - TLS reverse proxy; kiểm tra egress allowlist.
  - Secret runtime trên VM (không lưu trong GitHub).
  - Backup mã hóa lưu ngoài VM + **restore test**.
  - Log/alert về hệ thống giám sát; runbooks (`docs/runbooks/`).
  - Hoàn thiện pipeline deploy (đã có từ Phase 1): rollback đã diễn tập, backup timer, giám sát.
- Skills: `pace-deploy-vm`, `pace-security-review`, `pace-qa-testcases`, `pace-phase-gate`.
- **Exit:** 0 lỗ hổng High/Critical; restore test pass; runbook on-call; UAT dry-run với 2–3 user nội bộ pass; release candidate được tag.

## Phase 5 — Pilot (W13–W15)
- Sales (tuần 1–2) → IT (tuần 2–3); hỗ trợ hằng ngày; thu feedback chấm điểm brief.
- **KPI gate (PRD §9):** ≥3 team, ≥10 user, ≥30 run, ≥95% scheduled success, ≥90% claim có URL kiểm chứng, 0 truy cập chéo team trái phép, chi phí ≤ budget, Sales ≥4/5 trên ≥20 brief.
- **Exit:** `/pace-phase-gate` → báo cáo GO/NO-GO cho BOD.

## Phase 6 — P1 Enhancements (sau GO)
SP-01 SharePoint archive · AI-02 Weekly Review + Action Plan (chỉ từ brief đã duyệt) · COL-03 Outlook Calendar reminders · UX-02 Marketplace template-only sharing · Template thứ 2 cho phòng ban khác (HR/Marketing) để chứng minh tính nền tảng.

---

## Năng lực đội & buffer (ADR-011)
| Hạng mục | Dev-days |
|---|---:|
| P0 trong 06_MVP_BACKLOG | 105 |
| − P0-01..03 (Business/IT/BA làm, không tính dev) | −7 |
| − QA-01 (BA-PO/QA Lead làm chính) | −10 |
| + **UI-00** design system & AppShell (ADR-014, đã duyệt) | +3 |
| + **CMS-01** admin console & budget dashboard (ADR-014, đã duyệt) | +6 |
| **Tổng dev cần cho Phase 1–4** | **≈ 97** |
| Năng lực: 3 dev × 5 ngày × 75% tập trung × 10 tuần (W2–W12, trừ việc Phase 0) | ≈ 110 |
| **Buffer** | **≈ 12% (mỏng)** |
- Kết luận: giữ mốc **15 tuần**. Đội 4 người đủ để chạy kế hoạch nhưng buffer mỏng. Năng suất tăng nhờ agent là **upside, không tính vào cam kết**.
- Nếu trễ hơn 1 tuần ở cuối Phase 2, xem xét theo thứ tự:
  1. Dời COL-02 (Google Alerts) sang sau pilot; pilot chỉ dùng RSS.
  2. Thu gọn CMS-01: Policies/Audit chỉ đọc.
  3. Không cắt test bảo mật hay test ngân sách.

## Quản trị phê duyệt (ADR-011)
Chủ dự án là approver duy nhất, với SLA: plan story ≤ 1 ngày làm việc, gate report ≤ 2 ngày.

| Loại quyết định | Người duyệt |
|---|---|
| PR và plan story kỹ thuật | Tech Lead (ủy quyền) |
| AC và test case | BA-PO/QA (ủy quyền) |
| Phạm vi, ngân sách, gate GO/NO-GO, thay đổi bảo mật/credential | Chủ dự án |

Người viết code không tự merge PR của chính mình.

## Quy trình làm việc mỗi story (với Antigravity)
1. `/pace-story-kickoff <ID>` (Planning mode) → người duyệt plan (BA/Tech lead).
2. Agent code theo slice; chạy test sau mỗi slice; UI thì kiểm bằng browser agent.
3. `/pace-ux-review` (UI) · `/pace-security-review` (auth/gateway/collector/dispatch).
4. `/pace-story-done` → PR → review của người → merge.
5. Cuối phase: `/pace-phase-gate`.
