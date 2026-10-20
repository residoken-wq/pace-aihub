# HANDOFF — PACE AI Hub (bàn giao cho Claude Code, 20/10/2026)

> Đọc file này trước, sau đó đọc `AGENTS.md`, `docs/plan/PHASES.md` và `docs/adr/`. Spec gốc nằm ở `docs/specs/` (01–07 + prototype).

## 1. Dự án là gì
- **PACE AI Hub** là nền tảng nội bộ của PACE để **tạo, chạy, chia sẻ và quản trị AI Workflows** theo 3 cấp Personal / Team / Organization.
- **Không phải** website chia sẻ Claude API key. Nguyên tắc: *share spending capacity, never share the key*; chia sẻ tool ≠ chia sẻ dữ liệu ≠ chia sẻ credential.
- Use case MVP: **Sales Intelligence**. RSS/Google Alerts → Claude phân tích → DailyBrief JSON có nguồn, nhãn [Sự kiện]/[Suy luận], tối đa 5 tin/nhóm → duyệt → gửi Outlook.
- Kiến trúc:
  - Next.js (web/CMS) → FastAPI (auth BFF, RBAC, API) → Celery worker (collect/analyze/dispatch/reconcile) → PostgreSQL + Valkey.
  - **Claude Gateway** ở backend reserve budget **trước** khi gọi Anthropic.
  - Entra ID SSO. Power Automate chỉ dùng khi standard connector đáp ứng.
- Vai trò của Claude trong dự án: **Lead BA / Planner / QA**, kiêm hỗ trợ coding. Phải nói thẳng khi có rủi ro, không bịa version, giá hay nguồn.

## 2. Quyết định đã chốt (chi tiết: `docs/adr/ADR-009-015-decisions.md`, `docs/adr/ADR-013-tech-stack.md`)
| ADR | Quyết định |
|---|---|
| ADR-001..008 | Trong `docs/specs/07`: template builder (không canvas), gateway, Entra + RBAC, Postgres + SharePoint, PA chỉ standard connector, approval trước khi gửi, source allowlist, hard cap + reservation |
| ADR-009 | CI/CD **GitHub Actions**; image lên **GHCR** (private); deploy **pull-based** (VM tự kéo image), không dùng self-hosted runner |
| ADR-010 | Pilot trên **VM nội bộ** riêng (Ubuntu 24.04, Docker Compose); IT giao VM trước **22/10/2026**; egress allowlist |
| ADR-011 | Đội **4 người**: Tech Lead/BE, FE/UI, Fullstack/DevOps-Sec, BA-PO/QA. **Chủ dự án là approver duy nhất**. Tech Lead được ủy quyền duyệt PR; người viết không tự merge |
| ADR-012 | Được dùng AI coding agent với mã nguồn nội bộ. **Không** đưa secret/PII/dữ liệu thật vào prompt, fixture hay repo |
| ADR-013 | Tech stack: Node 24 LTS, pnpm 12, Next.js 16.4 + React 19.3 + Tailwind 4.3 + shadcn, Python 3.12 + FastAPI 0.150 + SQLAlchemy 2.1 + Alembic 1.20 + Pydantic 2.14, Celery 5.6, **Valkey 9.1** (không dùng Redis), **PostgreSQL 17**, Playwright 1.64. Auth = OIDC + PKCE tại FastAPI, session cookie HttpOnly, không giữ token ở browser. **Trạng thái: Accepted** (chủ dự án duyệt 20/10/2026) |
| ADR-014 | Thêm **UI-00** (design system + AppShell, +3 dev-days) và **CMS-01** (admin console + budget dashboard, +6) vào P0. P0 ≈ 114 dev-days |
| ADR-015 | Repo **tạm thời PUBLIC**. Không commit hostname/IP nội bộ, tenant ID, dữ liệu khách hàng/đối thủ thật; dùng `docs/internal/` và `tests/fixtures/private/` (gitignored). Hạn xem lại **30/10/2026** |

## 3. Kế hoạch (`docs/plan/PHASES.md`, kickoff 20/10/2026)
| Phase | Thời gian | Nội dung |
|---|---|---|
| 0 Gate 0 | 20/10–30/10 | Xác minh Anthropic API credit/billing, quyền Graph/PA, phân loại dữ liệu; repo + kit; nhận VM |
| 1 Foundation | 26/10–13/11 | INF-01a bootstrap, INF-01c walking skeleton lên VM, DB-01, AUTH-01, UI-00 |
| 2 Slice 1 | 16/11–04/12 | TOOL-01, UI-01 wizard, COL-01 RSS, GW-01, AI-01, manual run, preview |
| 3 Slice 2 | 07/12–25/12 | GW-02 reservation/ledger, scheduler, COL-02, approve/revision, OUT-01, OBS-01, CMS-01 |
| 4 Hardening | 28/12–08/01/2027 | QA-01, TLS, backup/restore test, runbooks |
| 5 Pilot | 11/01–29/01/2027 | Sales → IT; KPI gate; BOD GO/NO-GO trước Tết (nghỉ dự kiến 04–10/02/2027) |
| 6 P1 | Sau Tết | SP-01, AI-02, COL-03, UX-02 |
Buffer khoảng 12% (mỏng). Nếu trễ: dời COL-02 → thu gọn CMS-01. **Không** cắt test bảo mật hay test ngân sách.

## 4. Trạng thái repo hiện tại (`residoken-wq/pace-aihub`)
- `main`: commit `c903287` (kit + specs + spike + 20 fixtures tổng hợp), `6c15b19` (ADR-013 bản 1).
- Nhánh `docs/adr-013-tech-stack-review-2`, commit `53550e0`: ADR-013 bản 3 + xóa spec trùng ở `docs/*.md`. **Chưa có PR, chưa merge.**
- `apps/api/spikes/measure_brief.py`: spike đo token. Key đọc từ env, giá nhập tay. Không có secret.
- **Chưa có code ứng dụng.** INF-01a chưa bắt đầu.

## 5. Việc tiếp theo (theo thứ tự)
1. **Cập nhật kit trong repo (R2, chặn bootstrap).** `.agents/`, `AGENTS.md`, `docs/adr/ADR-009-015-decisions.md` trong repo là bản cũ, chưa có Next 16 / Node 24 / Valkey / quy tắc "không pin version theo trí nhớ". Chép đè từ kit v1.5+.
2. Trên nhánh review-2, sửa ADR-013:
   - Status → Accepted (sau khi chủ dự án đồng ý).
   - `401 UNAUTHORIZED` → `401 UNAUTHENTICATED` (theo spec 04).
   - Next.js EOL: "chính sách 2 năm, v16 ~10/2027".
   - Đổi tên cột "Ngày phát hành" → "Dòng major ra mắt".
   - Ghi chú trong traceability: AUTH-01 cần migration bảng `user_sessions` (thay đổi so với 03).
3. Mở PR vào `main`. Chủ dự án duyệt rồi mới merge.
4. **INF-01a**: `pace-repo-bootstrap` (monorepo, docker-compose dev, `ci.yml` + `build.yml`, Dependabot, pre-commit, gitleaks). Tra version thật trên npm/PyPI lúc bootstrap.
5. Rồi tới INF-01c (walking skeleton lên VM), DB-01, AUTH-01. AC bổ sung cho AUTH-01: session idle 8h / tối đa 24h (chờ chốt), kiểm tra `app_users.active` mỗi request (UAT-11), test IDOR cross-workspace.

## 6. Việc còn mở / cần người trả lời
| # | Việc | Ai | Hạn |
|---|---|---|---|
| 1 | Ký ADR-013 Accepted | Chủ dự án | Ngay |
| 2 | Chuyển repo sang **private** và vào **GitHub organization của PACE** (hiện ở tài khoản cá nhân, commit bằng gmail) | Chủ dự án | 30/10/2026 |
| 3 | Bằng chứng Anthropic Console: credit, billing, giá, spend limit. **Claude Team ≠ API miễn phí** | IT/Chủ dự án | Gate 0, 30/10 |
| 4 | Ma trận quyền Graph (mailbox chuyên dụng, Sites.Selected), Power Automate license | IT | Gate 0 |
| 5 | Phân loại dữ liệu / PII / retention (90d raw, 365d audit là đề xuất) | Data owner | Gate 0 |
| 6 | Thông số VM, domain nội bộ, nơi lưu backup | IT | 22/10/2026 |
| 7 | Chốt thời hạn session (idle/absolute) | Chủ dự án | Trước AUTH-01 |

## 7. Quy tắc làm việc (bắt buộc)
- Đọc spec trước khi code; trích ID (FR-xx, ADR-xxx, UAT-xx). Mâu thuẫn với spec → dừng lại và đề xuất ADR, không tự đổi phạm vi.
- Mỗi story: plan + AC Given/When/Then → duyệt → code theo lát nhỏ → test → cập nhật `docs/traceability.md` → PR. DoD: `.agents/rules/60-quality-gates.md`.
- Không bao giờ: lộ API key ra browser/log/repo; gọi Anthropic ngoài Gateway; auto-send khi chưa approve; dùng float cho tiền; query tenant data thiếu `workspace_id`.
- Version: luôn tra registry, không ghi theo trí nhớ. Thư viện không có LTS ghi "Rolling".
- Viết code và commit bằng tiếng Anh (conventional commits + story ID); UI tiếng Việt qua i18n; trao đổi với chủ dự án bằng tiếng Việt, kết luận trước, chi tiết sau.

## 8. Tài liệu ngoài repo
Claude Project "PACE AI Tool HUB" (claude.ai) chứa bản gốc 01–07, `claude/00_PROJECT_INSTRUCTIONS.md` (vai trò BA/Planning/QA), `claude/08_ANTIGRAVITY_SETUP_AND_PHASE_PLAN.md`, `claude/09_DECISION_LOG.md` (nhật ký quyết định + 3 vòng review ADR-013). Nếu có khác biệt, **repo là nguồn hiện hành cho code**, còn project là nguồn cho quyết định BA.
