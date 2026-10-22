# ADR-016: Giữ repo public đến Pilot, chuyển vào GitHub organization của PACE trước 11/01/2027
- **Status:** Proposed. Chuyển thành Accepted khi Chủ dự án merge PR chứa ADR này; bản merge đó được dùng làm **văn bản chấp nhận rủi ro** mà ADR-015 yêu cầu khi repo còn public sau 30/10/2026.
- **Date:** 2026-10-20 · **Deciders:** Chủ dự án · **Story:** INF-01, INF-01c, AUTH-01 · **Thay đổi:** hạn xem lại của ADR-015; một phần ADR-009 ("repo private")

## Context
- ADR-015 cho phép repo `residoken-wq/pace-aihub` tạm thời public, với hạn xem lại **30/10/2026**. Nếu sau mốc này repo vẫn public, Chủ dự án phải ký lại văn bản chấp nhận rủi ro, trước khi merge cấu hình AUTH-01 (Entra) và INF-01c (deploy lên VM).
- ADR-009 giả định repo private. HANDOFF mục 6.2 đặt hạn 30/10/2026 cho việc chuyển repo sang private và vào GitHub organization của PACE.
- Ngày 20/10/2026, Chủ dự án quyết định:
  1. Repo **giữ public**, trên tài khoản cá nhân hiện tại, đến khi lên production.
  2. "Production" là **Pilot, bắt đầu 11/01/2027** (Phase 5), khi Sales dùng thật với dữ liệu thật.
  3. Khi lên production, repo chuyển vào **GitHub organization của PACE**.

## Options considered
| Option | Pros | Cons | Cost/Risk |
|---|---|---|---|
| A. Private trên tài khoản cá nhân trước 30/10, vào org trước Pilot (khuyến nghị của BA/QA) | Gỡ gần hết rủi ro ADR-015 ngay; không tốn thêm chi phí | Vẫn phụ thuộc một tài khoản cá nhân đến khi chuyển org | Thấp |
| B. Giữ public đến 11/01/2027, rồi chuyển vào org và đặt private (**được chọn**) | Chủ dự án chủ động thời điểm; không đổi thiết lập trong lúc dựng nền | Thiết kế bảo mật, cấu trúc hạ tầng và lịch sử commit công khai trong khoảng 12 tuần, kể cả giai đoạn INF-01c và AUTH-01 | Trung bình; được chấp nhận kèm điều kiện bên dưới |
| C. Giữ public cả trong Pilot | Không phải chuyển | Dữ liệu và vận hành thật gắn với repo public và tài khoản cá nhân | Cao; loại |

## Decision
Chọn **B**.

1. Repo giữ public đến khi chuyển vào GitHub organization của PACE. Hạn chuyển: **trước 11/01/2027**. Khuyến nghị làm xong cùng mốc release candidate **08/01/2027**, không để đến ngày Pilot bắt đầu.
2. Khi chuyển vào organization, repo được đặt **private** ngay.
3. Toàn bộ điều kiện bắt buộc của ADR-015 tiếp tục áp dụng cho đến khi repo private.
4. **Điều kiện bổ sung** trong thời gian repo còn public:
   - **INF-01c (deploy VM):**
     - `compose.prod.yml`, script deploy và runbook trong repo chỉ dùng placeholder (ví dụ `pilot.example.invalid`).
     - Domain, hostname, IP, đường dẫn backup thật chỉ nằm trong file env trên VM hoặc trong `docs/internal/` (đã gitignore).
   - **AUTH-01 (Entra):**
     - Tenant ID, client ID và redirect URI thật chỉ nằm trong env trên VM hoặc trong GitHub Environment.
     - Không ghi các giá trị này trong code, test, fixture, docs hay mô tả PR.
   - **Thiết kế gateway và budget công khai:**
     - Chấp nhận rằng người ngoài đọc được thiết kế. Bảo mật không được dựa vào việc giấu thiết kế.
     - Ngưỡng hạn mức thật cấu hình trong DB qua CMS, không hard-code trong repo.
   - **GHCR:** package image đặt **private** ngay sau lần push đầu tiên. Việc này làm được dù repo public (ADR-015 điều kiện 4).
   - **Secret:**
     - Secret runtime không nằm trong GitHub (ADR-009).
     - Nếu có secret lọt lên repo, **rotate ngay** và báo Chủ dự án. Xoá commit không đủ, vì nội dung đã công khai.
5. **Điều kiện vào Phase 5 (Pilot):** repo đã nằm trong organization PACE và ở chế độ private. Nếu chưa đạt, Pilot không bắt đầu; việc này được ghi trong gate report.

## Consequences (incl. docs/specs to update)
- **Rủi ro được chấp nhận:** trong khoảng 20/10/2026 – 11/01/2027, mọi nội dung đã push được coi là **công khai vĩnh viễn**. Chuyển sang private sau đó không thu hồi được những gì người khác đã clone hoặc fork.
- **Phụ thuộc một tài khoản:** đến khi chuyển org, quyền admin repo, GHCR và GitHub Environments gắn với một tài khoản cá nhân. Chủ dự án giữ quyền truy cập và phải báo đội ngay nếu tài khoản có sự cố.
- **Checklist chuyển repo** (lập kế hoạch ở Phase 4, kiểm tra lại từng mục, vì không phải thiết lập nào cũng được GitHub tự chuyển theo):
  1. Transfer repo vào organization PACE, đặt private.
  2. Đổi tên image `ghcr.io/residoken-wq/...` sang namespace của organization; cập nhật `build.yml` và cấu hình deploy trên VM; package GHCR mới đặt private.
  3. Kiểm tra lại branch protection, CODEOWNERS, GitHub Environments (`dev`, `pilot`) cùng reviewer và secret, Dependabot, secret scanning và push protection, quyền của GitHub App.
  4. Thành viên đội commit bằng email công ty từ thời điểm chuyển.
  5. Cập nhật `AGENTS.md`, `CLAUDE.md`, `docs/HANDOFF.md`: bỏ các ghi chú "repo public".
- **Tài liệu cập nhật cùng ADR này:**
  - `docs/adr/ADR-009-015-decisions.md`: ADR-015 và R4 trỏ sang ADR-016.
  - `docs/HANDOFF.md`: mục 2 và 6.2.
  - `docs/plan/PHASES.md`: changelog, mốc lịch, điều kiện vào Phase 5.
  - `AGENTS.md`: danh sách ADR.

## Revisit trigger
- Có secret, hostname hay tenant ID thật lọt lên repo. Khi đó xem xét chuyển private ngay, không chờ Pilot.
- Data owner phân loại dữ liệu dự án từ mức Confidential trở lên (P0-03), hoặc IT Security yêu cầu repo private (ADR-012).
- Phát hiện fork hoặc clone đáng ngờ, hoặc workflow bị lạm dụng qua PR từ fork.
- Lịch Pilot dời. Hạn chuyển org dời theo, nhưng luôn **trước** ngày Pilot bắt đầu.
