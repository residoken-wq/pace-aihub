# 09 — Decision Log (bổ sung ADR-001..008 trong 07)
**Version:** 1.2 · **Ngày:** 20/10/2026 · **Nguồn:** trả lời của chủ dự án cho các câu hỏi mở trong `08_ANTIGRAVITY_SETUP_AND_PHASE_PLAN.md` v1.0 và v1.1

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
| ADR-015 | Repo GitHub **tạm thời public** | Accepted tạm thời, chủ dự án chấp nhận rủi ro; xem lại trước 30/10/2026 | Chủ dự án |
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
