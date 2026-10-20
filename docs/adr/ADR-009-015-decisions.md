# 09 — Decision Log (bổ sung ADR-001..008 trong 07)
**Version:** 1.5 · **Ngày:** 20/10/2026 · **Nguồn:** trả lời của chủ dự án cho các câu hỏi mở trong `08_ANTIGRAVITY_SETUP_AND_PHASE_PLAN.md` v1.0 và v1.1

**Changelog v1.5:**
- Review ADR-013 lần 3 (commit `53550e0`): đạt B1–B6, đề xuất Accepted. Còn lại: repo chưa cập nhật kit (R2), repo vẫn ở tài khoản cá nhân (R4).

**Changelog v1.4:**
- Review ADR-013 lần 2 (bản trong repo commit `6c15b19`): trả lại để sửa; kèm bảng version đã xác minh.

**Changelog v1.3:**
- ADR-013 (tech stack) bị trả lại để sửa: Next.js 14 hết hỗ trợ.

**Changelog v1.2:**
- Kickoff ngày 20/10/2026.
- ADR-015: repo GitHub tạm thời để public (rủi ro do chủ dự án chấp nhận, kèm điều kiện và hạn xem lại).

**Changelog v1.1:**
- Chủ dự án là người quyết định duy nhất về phân vai và phê duyệt.
- Xác nhận GitHub có secret scanning.
- IT bàn giao VM trong vòng 48h sau kickoff.
- Thêm ADR-014: đưa CMS-01 và UI-00 vào phạm vi P0.

| ADR | Quyết định | Trạng thái | Người phê duyệt |
|---|---|---|---|
| ADR-009 | CI/CD dùng **GitHub Actions** | Accepted | IT |
| ADR-010 | Pilot chạy trên **VM nội bộ** | Accepted | IT, BOD |
| ADR-011 | Đội delivery gồm **4 người**; chủ dự án quyết định phân vai và là approver duy nhất | Accepted | Chủ dự án |
| ADR-012 | Cho phép dùng **Antigravity + model của Antigravity** với mã nguồn nội bộ | Accepted | IT Security |
| ADR-013 | Tech stack: Node 24 LTS, Next.js 16.4 / React 19.3 / Tailwind 4.3, Python 3.12 + FastAPI 0.150, PostgreSQL 17, Valkey 9.1, BFF auth tại FastAPI | **Đề xuất Accepted** sau review lần 3 (commit `53550e0`), chờ chủ dự án ký; kèm 3 việc theo dõi | Chủ dự án |
| ADR-015 | Repo GitHub **tạm thời public** | Accepted tạm thời, chủ dự án chấp nhận rủi ro; hạn xem lại dời sang **trước 11/01/2027** theo [ADR-016](ADR-016-repo-visibility-until-pilot.md) | Chủ dự án |
| ADR-014 | Đưa **CMS-01** (admin console + budget dashboard) và **UI-00** (design system + AppShell) vào phạm vi P0 | Accepted | Chủ dự án (PO) |

---

## ADR-009 — CI/CD bằng GitHub Actions
- **Bối cảnh:** cần CI cho lint, test, migration, scan bảo mật và CD lên môi trường pilot.
- **Quyết định:** dùng GitHub Actions trên repo **private**. Image lưu ở GitHub Container Registry (GHCR, private).
- **Hệ quả:**
  - Runner do GitHub host chạy CI (build, test, scan), vì không cần vào mạng nội bộ.
  - Riêng CD vào VM nội bộ (ADR-010) phải chọn 1 trong 2 cách. Khuyến nghị **A**:
    - **A. Pull-based:** VM tự kéo image đã ký từ GHCR, chạy bằng script deploy do người chạy hoặc systemd timer. Không mở cổng inbound, không có runner trong mạng nội bộ.
    - **B. Self-hosted runner** đặt trong mạng nội bộ, chỉ phục vụ repo này, chạy với user không có quyền root, ephemeral. Không bao giờ dùng cho repo public hay PR từ fork.
  - Secrets: GitHub Environments (`dev`, `pilot`) với required reviewers cho `pilot`. **Secret runtime** (Anthropic key, Entra client secret, DB password) không nằm trong GitHub mà ở trên VM: file env mã hóa hoặc Vault/Key Vault.
  - Bảo vệ nhánh `main`: bắt buộc PR, CI xanh, 1 review của người, cấm force-push. Bật Dependabot. Gói GitHub của PACE **có** secret scanning (đã xác nhận 20/10/2026), nên bật bắt buộc **secret scanning + push protection** cho repo.
- **Xem lại khi:** PACE chuyển sang Azure DevOps, hoặc chính sách cấm lưu image ở GHCR.

## ADR-010 — Pilot trên VM nội bộ
- **Bối cảnh:** `02_SYSTEM_ARCHITECTURE` đề xuất VM Ubuntu 24.04 riêng, Docker Compose, có giới hạn egress; không triển khai lên SOC VM khi chưa đánh giá.
- **Quyết định:** pilot chạy trên VM nội bộ riêng, không dùng chung với SOC hay hệ thống khác.
- **Hệ quả / việc phải làm (Phase 0–1):**
  - Sizing đề xuất cho pilot (**giả định**, xác nhận khi load test ở Phase 4): 4 vCPU, 16 GB RAM, 100 GB SSD. Có thể tách thêm 1 VM cho Postgres nếu IT yêu cầu.
  - **Egress allowlist:** `api.anthropic.com`, `login.microsoftonline.com`, `graph.microsoft.com`, `ghcr.io`, các host RSS đã duyệt. Toàn bộ outbound đi qua proxy nếu IT bắt buộc.
  - **Inbound:** HTTPS 443 qua reverse proxy, chỉ trong mạng nội bộ/VPN. Chứng chỉ TLS nội bộ hoặc chứng chỉ public cho subdomain nội bộ.
  - Redirect URI của Entra app trỏ về domain nội bộ của pilot.
  - Backup Postgres mã hóa, lưu ngoài VM; restore test là exit criterion của Phase 4.
  - Log và alert đẩy về hệ thống giám sát hiện có (Wazuh nếu được duyệt).
- **Cam kết của IT (20/10/2026):** kickoff 20/10/2026, nên hạn bàn giao là **22/10/2026** (48h sau kickoff) gồm thông số VM, domain nội bộ, nơi lưu backup.
- **Hệ quả:** rủi ro chậm VM giảm từ Trung bình xuống Thấp. Kế hoạch chuyển sang **walking skeleton**: deploy bản khung lên VM ngay trong Phase 1, sau đó deploy liên tục, thay vì đợi đến W7–W8.
- Việc IT phải hoàn tất trong 48h: VM theo thông số đã chốt, domain + TLS, firewall egress allowlist, nơi lưu backup, tài khoản deploy (không phải root).
- **Xem lại khi:** chuyển sang production HA hoặc cloud.

## ADR-011 — Đội 4 người
- **Quyết định:** 4 người. **Chủ dự án là người quyết định duy nhất** về phân vai, phạm vi và phê duyệt gate. Bảng dưới là phân vai mặc định, áp dụng cho đến khi chủ dự án điều chỉnh:

| Vai | FTE | Trách nhiệm chính |
|---|---|---|
| Tech Lead / Backend | 1 | Kiến trúc, API, gateway, worker, review PR của agent |
| Frontend / UI | 1 | Next.js, design system, CMS/admin, e2e UI |
| Fullstack / DevOps-Sec | 1 | CI/CD, VM, collectors, Graph, bảo mật, backup |
| BA-PO / QA Lead | 1 | Backlog, AC, UAT, test plan, gate report, làm việc với Sales/BOD |

- **Năng lực ước tính:** 3 dev × 5 ngày × 75% thời gian tập trung ≈ **11 dev-days/tuần**.
- **Hệ quả lên kế hoạch:** giữ mốc 15 tuần, buffer khoảng 12%. Không rút ngắn timeline.
- **Rủi ro mới (key-person / nút cổ chai phê duyệt):** mọi quyết định dồn về một người.
  - SLA phản hồi: plan story ≤ 1 ngày làm việc; gate report ≤ 2 ngày.
  - Ủy quyền mặc định để không chặn đội:
    - Tech Lead duyệt PR và plan story kỹ thuật.
    - BA-PO/QA duyệt AC và test case.
    - Chủ dự án giữ quyền duyệt phạm vi, ngân sách, gate GO/NO-GO, và mọi thay đổi liên quan bảo mật/credential.
  - Phân tách nhiệm vụ: người viết code không tự merge PR của mình; reviewer báo cáo (approver) trong app không phải người cấu hình tool đó khi pilot.

## ADR-012 — Dùng Antigravity với mã nguồn nội bộ
- **Quyết định:** IT Security cho phép dùng Antigravity và các model đi kèm với mã nguồn PACE AI Hub.
- **Điều kiện bắt buộc (vẫn áp dụng):**
  - Không đưa secret, dữ liệu khách hàng thật, email thật hay PII vào prompt, fixture hoặc repo. Test dùng dữ liệu ẩn danh.
  - Dùng tài khoản công ty (không dùng tài khoản cá nhân) khi gói Antigravity hỗ trợ. Ghi nhận phiên bản/điều khoản dữ liệu tại thời điểm phê duyệt.
  - Terminal auto-execution: Request Review. Non-workspace file access: Off.
  - Mọi code do agent viết phải qua PR review của người và CI.
- **Xem lại khi:** điều khoản dữ liệu của Google thay đổi, hoặc dự án bắt đầu xử lý dữ liệu được phân loại Confidential trở lên.

## ADR-014 — Đưa CMS-01 và UI-00 vào phạm vi P0
- **Bối cảnh:** `05_UI_UX_SPEC` yêu cầu admin console (Team Management, Credentials, Policies, Audit) và budget dashboard, nhưng `06_MVP_BACKLOG` chưa có story riêng cho phần này. Design system/AppShell cũng chưa được ước lượng tách riêng.
- **Quyết định:** thêm 2 story vào P0:
  - **UI-00:** design tokens, shadcn primitives, AppShell, StatusBadge, 5-state patterns. +3 dev-days, Phase 1.
  - **CMS-01:** Admin console (Team Management, Credentials chỉ lưu vault ref, Policies gồm source allowlist/models/recipients, Audit viewer) + Budget dashboard. +6 dev-days, Phase 3.
- **Hệ quả:**
  - P0 tăng từ ≈105 lên ≈**114 dev-days**; phần dev cho Phase 1–4 ≈ 97/110, buffer ≈12%.
  - `06_MVP_BACKLOG` cần bổ sung 2 dòng này khi cập nhật bản tiếp theo.
  - Nếu cần cắt, CMS-01 có thể thu gọn (Policies/Audit chỉ xem) nhưng không bỏ hẳn, vì quản trị quota/thành viên là bắt buộc cho FR-09/FR-10.
- **Xem lại khi:** cuối Phase 2 nếu trễ hơn 1 tuần.

## ADR-015 — Repo GitHub tạm thời public
- **Bối cảnh:** chủ dự án chọn để repo public trong giai đoạn đầu (20/10/2026).
- **Khuyến nghị của BA/QA: chuyển sang private càng sớm càng tốt.**
  - Repo private trong GitHub organization không phát sinh thêm chi phí đáng kể.
  - Mọi thứ đã từng push lên repo public phải coi là **công khai vĩnh viễn**: người khác có thể đã clone hoặc fork, và đổi sang private sau này không thu hồi được lịch sử.
- **Rủi ro chính:**
  - Lộ secret, kể cả khi đã có secret scanning, vì không phải loại secret nào cũng được nhận diện.
  - Lộ thông tin nội bộ: hostname/IP của VM, tenant ID, danh sách khách hàng/đối thủ, mẫu email Google Alerts.
  - Lộ thiết kế bảo mật (threat model, cơ chế gateway/budget) cho người ngoài.
  - Tấn công qua GitHub Actions: PR từ fork, workflow injection.
  - Image trên GHCR có thể bị public theo repo.
- **Điều kiện bắt buộc khi repo còn public:**
  1. Không commit: `.env*`, hostname/IP/domain nội bộ, tenant/client ID, dữ liệu khách hàng/đối thủ thật, email/feeds thật, log. Thông tin hạ tầng nội bộ để ở `docs/internal/` (đã gitignore) hoặc trên VM.
  2. Fixtures và golden set chỉ dùng dữ liệu tổng hợp hoặc đã ẩn danh. Dữ liệu thật để ở `tests/fixtures/private/` (đã gitignore).
  3. GitHub Actions:
     - Bật "Require approval for all outside collaborators" cho workflow từ fork.
     - Không dùng `pull_request_target`.
     - **Không dùng self-hosted runner.**
     - Secret chỉ để trong Environment có reviewer; job PR không đọc được secret.
  4. Package GHCR đặt **private** (kiểm tra visibility sau lần push đầu tiên).
  5. Secret scanning + push protection bật (repo public cũng được hỗ trợ). Nếu có secret lọt lên: **rotate ngay**, không chỉ xóa commit.
  6. Thêm `LICENSE`; khuyến nghị "All rights reserved / proprietary" nếu không chủ đích open source.
- **Hạn xem lại:** **30/10/2026 (cuối W2)**, trước khi merge cấu hình AUTH-01 (Entra) và INF-01c (deploy lên VM). Nếu vẫn public sau mốc này, chủ dự án ký chấp nhận rủi ro lại bằng văn bản.
  - **Cập nhật 20/10/2026:** chủ dự án quyết định giữ public đến Pilot; repo chuyển vào GitHub organization của PACE và đặt private **trước 11/01/2027**, kèm điều kiện bổ sung. Xem [ADR-016](ADR-016-repo-visibility-until-pilot.md) (văn bản chấp nhận rủi ro).

## Review ADR-013 — lần 2 (20/10/2026, commit `6c15b19`, repo `residoken-wq/pace-aihub`)
**Kết luận: TRẢ LẠI ĐỂ SỬA.**
- Đạt: hướng kiến trúc (Next.js 16 + React 19 + Tailwind v4, BFF auth tại FastAPI, Valkey thay Redis, PostgreSQL 17, chính sách Dependabot).
- Chưa đạt: bảng version — nhiều pin cũ, có ngày EOL không có nguồn, và 2 thông tin sai.

### Lỗi chặn (phải sửa)
| # | Vấn đề | Bằng chứng (xác minh 20/10/2026) | Sửa |
|---|---|---|---|
| B1 | Pin version cũ khoảng 2 năm: FastAPI 0.115, Pydantic 2.10, Alembic 1.14, Celery 5.4, Playwright 1.49, Tailwind 4.0, pnpm 9, Valkey 8.0. Các thư viện này **không có LTS**; chỉ bản mới nhất được vá | PyPI/npm: FastAPI 0.150.0, Pydantic 2.14.1, SQLAlchemy 2.1.5, Alembic 1.20.0, Celery 5.6.3, Uvicorn 0.54.0, Playwright 1.64.1, Tailwind 4.3.3, pnpm 12.14.0, shadcn CLI 4.22.1, Next.js 16.4.2, React 19.3.1; Valkey tag mới nhất 9.1.2 | Dùng bảng chuẩn bên dưới |
| B2 | Cột EOL "≥ 2027/2028" cho thư viện không có chính sách LTS là **không có nguồn** (vi phạm nguyên tắc không bịa) | — | Ghi "Rolling: chỉ bản mới nhất được vá → Dependabot hàng tuần" |
| B3 | Sai: "PostgreSQL 18 chưa GA" | PostgreSQL 18 đã phát hành 09/2025, hiện có bản vá 18.6 | Sửa lập luận. Chọn 17 vẫn chấp nhận được (EOL 11/2029); hoặc 18 (EOL 11/2030) |
| B4 | Sai/lỗi thời: "Redis 7.4/8 không còn OSI open source" | Redis 8 (05/2025) có thêm lựa chọn license AGPLv3 | Giữ Valkey (BSD-3, tránh nghĩa vụ AGPL) nhưng sửa lập luận |
| B5 | Node.js 22 đã vào Maintenance từ 21/10/2025, EOL 30/04/2027, chỉ hơn mốc tối thiểu 1 tháng; production sẽ phải nâng cấp ngay | nodejs/Release schedule: Node 24 LTS, EOL 30/04/2028 | Dùng **Node 24 LTS** |
| B6 | Link `file:///c:/Users/admin/...` hỏng trên GitHub và lộ đường dẫn máy dev (repo public) | — | Đổi sang link tương đối (`../specs/01_PRD.md`) |

### Lỗi không chặn (nên sửa)
- "Expand/Contract (ADR-003)" sai tham chiếu: ADR-003 là Entra SSO. Nguồn đúng là rule `40-database`.
- Deciders: theo ADR-011, chủ dự án là approver duy nhất.
- Tailwind: Next.js dùng `app/globals.css`, không dùng `index.css`.
- Python 3.12 chỉ còn nhận bản vá bảo mật (EOL 10/2028, đạt tiêu chí). Khuyến nghị 3.13+ nếu mọi dependency có wheel; nếu giữ 3.12, ghi rõ lý do.
- Auth: bổ sung (a) cách thu hồi session khi offboard (FR-01, UAT-11) — xóa session trong Valkey + kiểm tra `active` mỗi request; (b) Valkey lưu session phải bật AOF, nếu không mọi người bị đăng xuất khi restart; (c) Next.js Server Components gọi API phải forward cookie qua mạng nội bộ, cùng origin qua reverse proxy (`/api` → FastAPI).
- Bỏ các tuyên bố tuyệt đối ("bảo mật tuyệt đối", "loại trừ IDOR"). BFF không chống IDOR; IDOR được kiểm soát bằng workspace filter + test.

### Bảng version chuẩn đề xuất (pin bản vá mới nhất tại ngày bootstrap)
| Thành phần | Pin | Hỗ trợ |
|---|---|---|
| Node.js | 24.x LTS (Krypton) | EOL 30/04/2028 |
| pnpm | 12.x | Rolling |
| Next.js / React | 16.4.x / 19.3.x | Next 16: EOL ~10/2027 theo chính sách 2 năm |
| Tailwind CSS / shadcn CLI | 4.3.x / 4.x | Rolling |
| Playwright | 1.64.x | Rolling |
| Python | 3.13.x (hoặc 3.12.x có lý do) | 3.12: EOL 10/2028 |
| FastAPI / Uvicorn | 0.150.x / 0.54.x | Rolling |
| Pydantic | 2.14.x | Rolling (v2) |
| SQLAlchemy / Alembic | 2.1.x / 1.20.x | Rolling |
| Celery | 5.6.x | Rolling |
| Valkey | 9.1.x | Theo chính sách Valkey (agent xác minh, ghi link) |
| PostgreSQL | 17.x (hoặc 18.x) | 17: EOL 11/2029 |

### Phát hiện về repo (ngoài ADR-013)
| # | Mức | Vấn đề | Sửa |
|---|---|---|---|
| R1 | Trung bình | Tài liệu spec bị nhân đôi: `docs/*.md` (bản cũ, 06 chưa có ADR-014) và `docs/specs/*.md`. Agent có thể đọc nhầm bản cũ | Xóa bản ở `docs/` gốc, chỉ giữ `docs/specs/` |
| R2 | Trung bình | Repo đang dùng kit cũ (v1.3): AGENTS.md, rule 30, skill bootstrap, tokens.css **chưa có** Next.js 16 / Tailwind v4 | Chép đè kit v1.4+ (`.agents/`, `AGENTS.md`) |
| R3 | Thấp | Spike `apps/api/spikes/measure_brief.py` commit thẳng vào `main` (prompt yêu cầu không commit vào main). Đã kiểm: key đọc từ env, giá nhập tay, không có secret | Chấp nhận; chuyển sang `spikes/` ngoài `apps/` hoặc giữ nhưng loại khỏi build |
| R4 | Trung bình | Repo nằm ở tài khoản cá nhân `residoken-wq` (commit bằng email gmail), không phải GitHub organization của PACE như ADR-009/012 | Chuyển repo vào organization PACE; dùng tài khoản công ty |
| R5 | Đạt | 20 fixture nguồn là dữ liệu tổng hợp (`example.com`, "Tập đoàn Alpha", "CompetitorY"); không thấy secret, IP hay hostname nội bộ | — |

## Review ADR-013 — lần 3 (20/10/2026, commit `53550e0`, nhánh `docs/adr-013-tech-stack-review-2`)
**Kết luận: ĐỀ XUẤT ACCEPTED.** Cả 6 lỗi chặn B1–B6 đã được sửa.

| # | Kết quả |
|---|---|
| B1 Version cũ | Đạt: version khớp registry ngày 20/10/2026 |
| B2 EOL không có nguồn | Đạt: dùng "Rolling" |
| B3 PostgreSQL 18 | Đạt: đã sửa lập luận, giữ 17 có lý do |
| B4 Redis license | Đạt: đã nêu AGPLv3, giữ Valkey |
| B5 Node.js | Đạt: Node 24 LTS |
| B6 Link file:/// | Đạt: dùng link tương đối |
| Spec trùng (R1) | Đạt: đã xóa `docs/*.md`, chỉ giữ `docs/specs/` |

**Việc theo dõi (không chặn, sửa trong PR này hoặc trong AUTH-01):**
1. Mã lỗi: ADR ghi `401 UNAUTHORIZED`, spec 04 dùng `401 UNAUTHENTICATED`. Phải theo 04.
2. **Thay đổi schema:** ADR thêm bảng `user_sessions` (`revoked_at`) chưa có trong `03_DATABASE_SCHEMA.sql`. Chấp nhận; tạo migration trong AUTH-01 và ghi vào traceability.
3. AC bổ sung cho AUTH-01: phát hiện tài khoản bị disable trong Entra. Session có thời hạn (đề xuất idle 8h, tối đa 24h; chờ chủ dự án chốt), kiểm tra lại `app_users.active` mỗi request, đăng nhập lại khi hết hạn. Nếu không có cơ chế này, UAT-11 chỉ đạt khi admin thu hồi thủ công trong CMS.
4. Nhỏ:
   - Next.js không phải "Rolling" mà có chính sách hỗ trợ 2 năm (v16 hết hỗ trợ khoảng 10/2027).
   - Cột "Ngày phát hành" ghi ngày của dòng major, không phải ngày của bản pin (vd FastAPI 0.150 không phát hành 2024-09). Đổi tên cột thành "Dòng major ra mắt".
   - AGPLv3 chỉ buộc công bố mã khi **sửa đổi** Redis và cung cấp qua mạng; lập luận hiện tại hơi quá, nhưng không ảnh hưởng quyết định chọn Valkey.

**Điều kiện trước khi chạy INF-01a (`/pace-repo-bootstrap`):**
- **R2 (chặn bootstrap):** repo vẫn dùng kit cũ. `AGENTS.md`, rule `30-frontend-nextjs`, skill `pace-repo-bootstrap` chưa có Next.js 16 / Node 24 / Valkey / quy tắc "không pin version theo trí nhớ". Phải chép đè kit v1.5 trước khi bootstrap, nếu không agent sẽ làm theo skill cũ.
- Merge nhánh `docs/adr-013-tech-stack-review-2` vào `main` qua PR (không push thẳng).
- R4 (chưa chặn): chuyển repo vào GitHub organization của PACE. Hạn dời sang trước 11/01/2027 theo [ADR-016](ADR-016-repo-visibility-until-pilot.md).
