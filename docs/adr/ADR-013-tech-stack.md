# ADR-013: Chuẩn hoá Tech Stack và phiên bản cho PACE AI Hub
- **Status:** Proposed
- **Date:** 2026-10-20 · **Deciders:** Tech Lead, Chủ dự án, IT Platform Lead, BA-PO · **Story:** INF-01a, DB-01, UI-00

---

## 1. Context (Bối cảnh)
Theo [01_PRD.md](file:///c:/Users/admin/Documents/GitHub/pace-aihub/docs/specs/01_PRD.md), [02_SYSTEM_ARCHITECTURE.md](file:///c:/Users/admin/Documents/GitHub/pace-aihub/docs/specs/02_SYSTEM_ARCHITECTURE.md), [AGENTS.md](file:///c:/Users/admin/Documents/GitHub/pace-aihub/AGENTS.md) và [PHASES.md](file:///c:/Users/admin/Documents/GitHub/pace-aihub/docs/plan/PHASES.md), PACE AI Hub là nền tảng quản trị AI workflow tập trung dành cho nội bộ PACE. Hệ thống yêu cầu:
- Tự phục vụ an toàn (self-service AI Tool Catalog), chia sẻ hạn mức ngân sách chi tiêu thay vì chia sẻ Claude API key.
- Phân quyền nghiêm ngặt theo workspace (Personal, Team, Org), phòng chống triệt để rò rỉ dữ liệu chéo (IDOR) và bảo đảm tính toàn vẹn kiểm toán (Audit).
- Kiến trúc monorepo phân tách rõ giữa frontend giao diện/CMS quản trị, API điều phối & quản trị ngân sách, và tiến trình worker chạy nền (thu thập tin, sinh báo cáo qua Claude Gateway, dispatch email).
- Tuân thủ các quyết định đã phê duyệt trong [ADR-009-015-decisions.md](file:///c:/Users/admin/Documents/GitHub/pace-aihub/docs/adr/ADR-009-015-decisions.md):
  - **ADR-009:** CI/CD bằng GitHub Actions (build, test, push image lên GHCR).
  - **ADR-010:** Môi trường Pilot chạy trên VM nội bộ riêng biệt (Ubuntu 24.04 LTS), triển khai dạng pull-based container qua Docker Compose, cô lập egress mạng.
  - **ADR-011:** Đội ngũ tinh gọn 4 người (Tech Lead/BE, FE/UI, Fullstack/DevOps-Sec, BA-PO/QA Lead).
  - **ADR-012:** Cho phép Antigravity hỗ trợ lập trình với nguyên tắc không lưu trữ secret hay PII thật trong mã nguồn/prompt.
  - **ADR-014:** Đưa CMS-01 và UI-00 vào phạm vi P0.
  - **ADR-015:** Repo GitHub tạm thời để public, kiểm soát tuyệt đối secret qua biến môi trường/vault, loại trừ toàn bộ dữ liệu nội bộ/private.

### Tiêu chuẩn vòng đời (Lifecycle Requirement):
Tại thời điểm kickoff (20/10/2026), Next.js 14 đã kết thúc vòng đời hỗ trợ (EOL: 26/10/2025), Next.js 15 kết thúc vòng đời vào 21/10/2026. Để đảm bảo dự án vận hành an toàn qua các giai đoạn Pilot và vận hành chính thức, **tất cả các thành phần trong toàn bộ tech stack bắt buộc phải có ngày hết hạn hỗ trợ (EOL) sau ngày 31/03/2027.**

---

## 2. Bảng thông số chi tiết toàn bộ các thành phần (Components & Lifecycle)

Tất cả các thành phần công nghệ được cố định phiên bản (pin version), có ngày phát hành, ngày EOL chính thức sau 31/03/2027 và link nguồn tài liệu chính thức:

| Tên thành phần | Phiên bản cố định (Pin version) | Ngày phát hành | Ngày hết hỗ trợ (EOL) | Link nguồn chính thức |
|---|---|---|---|---|
| **Node.js (LTS)** | `22.x LTS` (Jod) | 2024-04-23 (LTS: 2024-10-29) | 2027-04-30 | https://nodejs.org/en/about/previous-releases |
| **pnpm** | `9.12.x` / `9.x` | 2024-04-16 | Hỗ trợ theo Node 22 (≥ 2027-04-30) | https://pnpm.io/ |
| **Next.js** | `16.x` (Bản vá mới nhất) | 2025-10-21 | Q4/2027 (Sau 31/03/2027) | https://nextjs.org/blog |
| **React** | `19.x` | 2024-12-05 | Kéo dài theo React 19 cycle (≥ 2028) | https://react.dev/blog/2024/12/05/react-19 |
| **Tailwind CSS** | `v4.0.x` | 2025-01-23 | Kéo dài theo Tailwind v4 cycle (≥ 2028) | https://tailwindcss.com/blog/tailwindcss-v4 |
| **shadcn/ui** | `latest CLI` (hỗ trợ TW v4) | 2025-01 | Mã nguồn mở thuộc codebase (bảo trì nội bộ) | https://ui.shadcn.com/docs/changelog |
| **Python** | `3.12.x` | 2023-10-02 | 2028-10-31 | https://devguide.python.org/versions/ |
| **FastAPI** | `0.115.x` | 2024-09-19 | Active maintenance (hỗ trợ dài hạn ≥ 2027) | https://fastapi.tiangolo.com/release-notes/ |
| **SQLAlchemy** | `2.0.x` (2.0.36+) | 2023-01-26 | Nhánh chính thức LTS 2.0 (≥ 2028) | https://www.sqlalchemy.org/download.html |
| **Alembic** | `1.14.x` | 2024-11-13 | Đồng hành cùng SQLAlchemy 2.0 (≥ 2028) | https://alembic.sqlalchemy.org/ |
| **Pydantic** | `2.10.x` | 2024-11-20 | Nhánh chính thức Pydantic v2 (≥ 2028) | https://docs.pydantic.dev/latest/changelog/ |
| **Celery** | `5.4.x` | 2024-04-17 | Active maintenance dòng 5.x (≥ 2027-06) | https://docs.celeryq.dev/en/stable/history/changelog-5.4.html |
| **Valkey** (thay thế Redis) | `8.0.x` | 2024-09-12 | 2028-09 (Dự án Linux Foundation) | https://valkey.io/ |
| **PostgreSQL** | `17.x` | 2024-09-26 | 2029-11-08 | https://www.postgresql.org/support/versioning/ |
| **Playwright** | `1.49.x` | 2024-11-21 | Active maintenance bởi Microsoft (≥ 2027) | https://playwright.dev/ |

---

## 3. Phân tích chi tiết và Lựa chọn chuyên biệt

### 3.1. Frontend Web App & CMS: Next.js 16 + Tailwind CSS v4 + shadcn/ui
- **Next.js 16.x & React 19:** Next.js 14 đã chính thức EOL vào 26/10/2025, Next.js 15 EOL vào 21/10/2026. Bắt buộc pin Next.js 16.x bản vá ổn định mới nhất kết hợp React 19. Mô hình Server Components mặc định, tối ưu hóa xử lý bảo mật cho phiên làm việc không lưu trữ token client.
- **Tailwind CSS v4:** Chuyển sang engine Oxide viết bằng Rust, cấu hình thuần CSS hiện đại (`@theme`), tốc độ biên dịch nhanh gấp 5-10 lần, không cần file `tailwind.config.js` cồng kềnh.
- **shadcn/ui (phiên bản tương thích Tailwind v4):** Sử dụng các component primitives chuẩn hóa từ Radix UI / Base UI đã cập nhật hỗ trợ CSS variables và Tailwind v4. Toàn bộ mã nguồn component nằm trong repo (`components/ui/`), tuân thủ triệt để design token tại `.agents/skills/pace-design-system`.

### 3.2. Caching & Message Broker: Chuyển từ Redis sang Valkey 8.0
- **Lý do pháp lý và bản quyền:** Từ tháng 03/2024, Redis Ltd. đã hủy bỏ bản quyền nguồn mở tự do (BSD-3-Clause) từ bản Redis 7.4 và 8.0, chuyển sang dual-license RSALv2 / SSPLv1 (không còn được OSI công nhận là mã nguồn mở, gây rủi ro pháp lý cho các giải pháp nội bộ doanh nghiệp). Redis 7.2 là bản BSD cuối cùng nhưng vòng đời hỗ trợ sẽ kết thúc sớm.
- **Giải pháp Valkey 8.0:** Valkey là dự án fork mã nguồn mở phi lợi nhuận được bảo trợ bởi Linux Foundation (với sự đóng góp của AWS, Google, Microsoft, Ericsson...). Valkey 8.0:
  - Duy trì giấy phép **BSD-3-Clause** hoàn toàn miễn phí và tự do.
  - Tương thích 100% drop-in replacement với Redis protocol và các thư viện `redis-py`, Celery broker mà không cần thay đổi code.
  - Vòng đời hỗ trợ của Valkey 8.0 kéo dài đến tháng 09/2028 (vượt xa mốc 31/03/2027).

### 3.3. Hệ quản trị cơ sở dữ liệu: So sánh PostgreSQL 16, 17 và 18
- **PostgreSQL 16:** Phát hành 2023-09-14, EOL: 2028-11-09. Mặc định có sẵn trên Ubuntu 24.04, ổn định cao nhưng thiếu các tối ưu JSON mới.
- **PostgreSQL 17 (ĐƯỢC CHỌN):**
  - Phát hành ngày 26/09/2024, **EOL: 08/11/2029** (hơn 3 năm sau mốc tối thiểu 31/03/2027).
  - Tối ưu bộ nhớ vượt trội: Cơ chế VACUUM thế hệ mới tiêu thụ bộ nhớ RAM ít hơn tới 20 lần, giảm nguy cơ thắt cổ chai I/O trên VM pilot (ADR-010).
  - **Tối ưu JSON/JSONB chuẩn SQL:2023:** Bổ sung `JSON_TABLE` và hàm xử lý JSON trực tiếp với hiệu năng cao, cực kỳ thiết yếu cho schema `DailyBrief` dạng JSON cấu trúc và truy vấn lịch sử trong `audit_events`.
  - Hiệu năng truy vấn `IN` / `ANY` trên tenant isolation (`workspace_id`) nhanh hơn rõ rệt.
- **PostgreSQL 18:** Dự kiến phát hành cuối 2025/2026, chưa có bản GA kiểm chứng thực tế và chưa phù hợp cho dự án triển khai tức thì.
- **Kết luận:** **Chọn PostgreSQL 17.x** (cài đặt qua repository PGDG chính thức trên Ubuntu 24.04).

---

## 4. Kiến trúc xác thực & Luồng đăng nhập (BFF Pattern tại FastAPI)

Tuân thủ nghiêm ngặt nguyên tắc của [10-security.md](file:///c:/Users/admin/Documents/GitHub/pace-aihub/.agents/rules/10-security.md): **Không bao giờ lưu access token hay secret ở browser hoặc Next.js client.**

### 4.1. Nguyên tắc cốt lõi:
1. **FastAPI đóng vai trò Backend-for-Frontend (BFF) độc quyền xử lý Auth:** Toàn bộ quá trình bắt tay OIDC với Microsoft Entra ID (PKCE, đổi mã authorization code lấy tokens) diễn ra hoàn toàn tại backend FastAPI.
2. **Next.js không lưu trữ Access Token:** Browser và Next.js Client Components **không bao giờ** nhìn thấy, lưu trữ hay giải mã Access Token hoặc ID Token của Entra ID.
3. **Không dùng thư viện Auth lưu token ở client:** Nghiêm cấm dùng `msal-browser`, NextAuth lưu JWT phía client, hoặc lưu token vào `localStorage` / `sessionStorage`.
4. **Session Cookie an toàn tuyệt đối:** Trình duyệt chỉ nhận và lưu duy nhất một Server-Side Session Cookie với các thuộc tính:
   - `HttpOnly`: JavaScript phía trình duyệt không thể truy cập (chống XSS đánh cắp session).
   - `Secure`: Chỉ truyền qua giao thức HTTPS.
   - `SameSite=Lax` (hoặc `Strict` cho các API nhạy cảm): Chống tấn công CSRF.
   - `Path=/`.
5. **Bảo vệ CSRF:** Mọi request thay đổi trạng thái (POST, PUT, DELETE, PATCH) đều yêu cầu Anti-CSRF token hoặc custom header (`X-Requested-With: XMLHttpRequest` / `X-CSRF-Token`).

### 4.2. Sơ đồ tuần tự luồng đăng nhập (OIDC + Session Flow):

```mermaid
sequenceDiagram
    autonumber
    actor User as Người dùng (Browser)
    participant Web as Next.js Web App (apps/web)
    participant Proxy as Reverse Proxy (Traefik/Nginx)
    participant API as FastAPI BFF (apps/api)
    participant DB as Database & Valkey
    participant Entra as Microsoft Entra ID (OIDC)

    User->>Web: 1. Bấm "Đăng nhập với Microsoft"
    Web->>Proxy: 2. Điều hướng GET /api/v1/auth/login
    Proxy->>API: Chuyển tiếp tới FastAPI
    API->>API: 3. Tạo code_verifier, code_challenge (PKCE), state, nonce
    API->>DB: 4. Lưu tạm PKCE state vào Valkey (TTL 5 phút)
    API-->>User: 5. 302 Redirect tới login.microsoftonline.com
    User->>Entra: 6. Đăng nhập & đồng ý quyền (SSO PACE)
    Entra-->>User: 7. 302 Redirect về /api/v1/auth/callback?code=...&state=...
    User->>Proxy: 8. GET /api/v1/auth/callback?code=...&state=...
    Proxy->>API: Chuyển tiếp tới FastAPI
    API->>DB: 9. Kiểm tra & xác thực state từ Valkey
    API->>Entra: 10. POST /token (back-channel: đổi code + code_verifier)
    Entra-->>API: 11. Trả về id_token, access_token (server-side only)
    API->>DB: 12. Xác thực user/workspace trong PostgreSQL, tạo session_token trong Valkey
    API-->>User: 13. Set-Cookie: pace_session=<session_token>; HttpOnly; Secure; SameSite=Lax
    API-->>User: 14. 302 Redirect về trang chủ (/)
    User->>Web: 15. Truy cập giao diện (Cookie tự động đính kèm)
    Web->>Proxy: 16. Gọi dữ liệu API (GET /api/v1/users/me) kèm Cookie
    Proxy->>API: Chuyển tiếp request
    API->>DB: 17. Tra cứu session, nạp workspace RBAC context
    API-->>Web: 18. Trả về thông tin user & quyền hạn (JSON)
```

---

## 5. Rủi ro & Cách nâng cấp cho từng thành phần (Risks & Upgrade Strategy)

| Thành phần | Rủi ro tiềm ẩn | Chiến lược & Cách thức nâng cấp |
|---|---|---|
| **Node.js 22 LTS** | Khi chuẩn bị chuyển sang Node 24 LTS (2025-2026), một số native packages có thể cần rebuild. | Node 22 hỗ trợ đến 04/2027. Nâng cấp bằng cách cập nhật Docker base image `node:22-alpine` $\rightarrow$ `node:24-alpine` và chạy test CI. |
| **pnpm 9.x** | Thay đổi format lockfile khi lên bản 10. | Chạy `pnpm import` hoặc `pnpm install` cập nhật lockfile trong PR riêng, kiểm thử `pnpm install --frozen-lockfile` trên CI. |
| **Next.js 16 & React 19** | Thay đổi trong React 19 Actions hoặc Server Components APIs. | Khóa version chính xác (pin exact patch trong `package.json`). Chỉ dùng các API đã ổn định, tách biệt client components ra lá giao diện (`"use client"`). |
| **Tailwind CSS v4 & shadcn/ui** | Một số plugin cộng đồng của Tailwind v3 chưa tương thích với engine CSS-first v4. | Không dùng plugin bên thứ ba ngoài danh mục đã kiểm duyệt; cấu hình theme trực tiếp qua CSS variables tại `index.css`. Code shadcn/ui lưu nội bộ nên dễ tinh chỉnh trực tiếp. |
| **Python 3.12 & FastAPI** | Deprecation các thư viện cũ liên quan đến asyncio. | Sử dụng `uv` quản lý lockfile `uv.lock`. FastAPI và Starlette có độ tương thích cao; kiểm thử tự động với `pytest` và `mypy --strict`. |
| **SQLAlchemy 2.0 & Alembic** | Xung đột locking transaction khi migrate database đang chạy. | Áp dụng nguyên tắc Expand/Contract (ADR-003): mọi migration đều có hàm `downgrade()`, kiểm thử up $\rightarrow$ down $\rightarrow$ up trên testcontainers Postgres thật trước khi merge. |
| **Pydantic v2** | Hiệu năng serialize object phức tạp hoặc custom validator. | Tận dụng Rust core của Pydantic v2. Schema validation cho `DailyBrief` được bọc try/except và ghi log chi tiết lỗi schema mismatch. |
| **Celery 5.4 & Valkey 8.0** | Task bị timeout hoặc mất kết nối broker khi VM khởi động lại. | Valkey bật chế độ lưu trữ bền vững (AOF/RDB persistence volume). Celery cấu hình `acks_late=True`, `task_reject_on_worker_lost=True`, giới hạn retry có jitter và định tuyến lỗi sang Dead-Letter Queue (DLQ). |
| **PostgreSQL 17** | Nâng cấp major version cần dump/restore hoặc `pg_upgrade`. | Phiên bản 17 có EOL đến tận tháng 11/2029 (không cần nâng cấp major trong toàn bộ vòng đời pilot và mở rộng ban đầu). Backup định kỳ bằng `pg_dump` vào thư mục ngoài VM theo runbook. |
| **Playwright** | Browser binaries thay đổi hoặc flaky test do độ trễ mạng. | Cố định phiên bản Playwright; CI sử dụng cache browser binaries; kịch bản test sử dụng locator ngữ nghĩa (`getByRole`, `getByTestId`) thay vì XPath/CSS class. |

---

## 6. Chính sách cập nhật bản vá (Patching & Dependency Policy)

Để đảm bảo hệ thống luôn được bảo vệ khỏi các lỗ hổng bảo mật (CVE) mà không gây gián đoạn tính ổn định:

1. **Cấu hình công cụ tự động:**
   - Sử dụng **Dependabot** (hoặc Renovate) tích hợp trực tiếp trên GitHub repository.
   - Bật **GitHub Secret Scanning** và **Push Protection** (ADR-015).
2. **Tần suất quét và kiểm tra:**
   - Quét định kỳ hàng tuần (**Weekly vào thứ Hai lúc 08:00 Asia/Ho_Chi_Minh**).
3. **Quy trình xử lý PR phụ thuộc:**
   - **Patch updates (x.y.Z $\rightarrow$ x.y.Z+1):** Dependabot tự động mở PR. GitHub Actions chạy toàn bộ test matrix (lint, typecheck, pytest, playwright e2e). Nếu tất cả test xanh và không có cảnh báo bảo mật, PR được phép merge nhanh sau khi Tech Lead duyệt.
   - **Minor updates (x.Y.z $\rightarrow$ x.Y+1.0):** Yêu cầu kiểm tra kỹ changelog, chạy test thủ công và staging trước khi merge.
   - **Major updates (X.y.z $\rightarrow$ X+1.0.0):** Không tự động merge; chỉ thực hiện theo kế hoạch nâng cấp riêng được phê duyệt bằng ADR.
4. **Quy trình khẩn cấp với lỗ hổng nghiêm trọng (Critical/High CVE):**
   - Khi có cảnh báo bảo mật CVE mức High/Critical từ GitHub Dependabot Alerts, đội dự án kích hoạt quy trình nóng: kiểm tra PoC, cập nhật bản vá và triển khai lại lên VM trong vòng **24 giờ**.

---

## 7. Consequences (Hệ quả và tác động)

### 7.1. Tác động tích cực
- **Đáp ứng 100% tiêu chí EOL:** Mọi thành phần đều có thời hạn hỗ trợ chính thức tối thiểu đến tháng 04/2027 (Node 22), tháng 10/2028 (Python 3.12, Valkey 8) và tháng 11/2029 (PostgreSQL 17).
- **An toàn pháp lý doanh nghiệp:** Loại bỏ hoàn toàn rủi ro bản quyền của Redis 7.4+ bằng cách chuyển sang Valkey 8.0 (Linux Foundation, BSD-3-Clause).
- **Bảo mật tuyệt đối luồng dữ liệu:** Mô hình BFF tại FastAPI ngăn chặn triệt để nguy cơ lộ Access Token ở client; loại trừ lỗi IDOR và XSS token theft.
- **Hiệu năng và trải nghiệm hiện đại:** Next.js 16 và Tailwind CSS v4 mang lại tốc độ biên dịch và giao diện đạt chuẩn cao cấp nhất theo [pace-design-system](file:///c:/Users/admin/Documents/GitHub/pace-aihub/.agents/skills/pace-design-system).

### 7.2. Việc cần làm tiếp theo
1. Trình Chủ dự án và Tech Lead review tài liệu này.
2. Sau khi được duyệt, chuyển trạng thái từ `Proposed` sang `Accepted`.
3. Bắt đầu Phase 1 với Story **INF-01a** (`/pace-repo-bootstrap`) khởi tạo monorepo khớp chính xác các phiên bản đã pin trong tài liệu này.