# ADR-013: Chuẩn hoá Tech Stack và phiên bản cho PACE AI Hub
- **Status:** Proposed
- **Date:** 2026-10-20 · **Deciders:** Chủ dự án · **Story:** INF-01a, DB-01, UI-00

---

## 1. Context (Bối cảnh)
Theo [01_PRD.md](../specs/01_PRD.md), [02_SYSTEM_ARCHITECTURE.md](../specs/02_SYSTEM_ARCHITECTURE.md), [AGENTS.md](../../AGENTS.md) và [PHASES.md](../plan/PHASES.md), PACE AI Hub là nền tảng quản trị AI workflow tập trung dành cho nội bộ PACE. Hệ thống yêu cầu:
- Tự phục vụ (self-service AI Tool Catalog), chia sẻ hạn mức ngân sách chi tiêu thay vì chia sẻ Claude API key.
- Phân quyền theo workspace (Personal, Team, Org), phòng chống rò rỉ dữ liệu chéo (IDOR) qua cơ chế kiểm tra quyền bắt buộc tại tầng repository và ghi nhận kiểm toán (Audit).
- Kiến trúc monorepo phân tách rõ giữa frontend giao diện/CMS quản trị, API điều phối & quản trị ngân sách, và tiến trình worker chạy nền (thu thập tin, sinh báo cáo qua Claude Gateway, dispatch email).
- Tuân thủ các quyết định đã phê duyệt trong [ADR-009-015-decisions.md](ADR-009-015-decisions.md):
  - **ADR-009:** CI/CD bằng GitHub Actions (build, test, push image lên GHCR).
  - **ADR-010:** Môi trường Pilot chạy trên VM nội bộ riêng biệt (Ubuntu 24.04 LTS), triển khai dạng pull-based container qua Docker Compose, cô lập egress mạng.
  - **ADR-011:** Đội ngũ tinh gọn 4 người (Tech Lead/BE, FE/UI, Fullstack/DevOps-Sec, BA-PO/QA Lead), trong đó Chủ dự án là người quyết định duy nhất.
  - **ADR-012:** Cho phép Antigravity hỗ trợ lập trình với nguyên tắc không lưu trữ secret hay PII thật trong mã nguồn/prompt.
  - **ADR-014:** Đưa CMS-01 và UI-00 vào phạm vi P0.
  - **ADR-015:** Repo GitHub tạm thời để public, kiểm soát secret qua biến môi trường/vault, loại trừ toàn bộ dữ liệu nội bộ/private.

### Tiêu chuẩn vòng đời (Lifecycle Requirement):
Tại thời điểm kickoff (20/10/2026), Next.js 14 đã kết thúc vòng đời hỗ trợ (EOL: 26/10/2025), Next.js 15 kết thúc vòng đời vào 21/10/2026. Để đảm bảo hệ thống vận hành an toàn qua các giai đoạn Pilot và vận hành chính thức, **tất cả các nền tảng có chính sách LTS/versioning bắt buộc phải có ngày hết hạn hỗ trợ (EOL) sau ngày 31/03/2027**. Đối với các thư viện không áp dụng chính sách LTS, áp dụng mô hình rolling update theo bản mới nhất được phát hành và kiểm thử tự động.

---

## 2. Bảng thông số chi tiết toàn bộ các thành phần (Components & Lifecycle)

Toàn bộ các thành phần được tra cứu trực tiếp từ registry (`npm view` và PyPI API) và cố định phiên bản (pin version) tại thời điểm lập tài liệu:

| Tên thành phần | Phiên bản cố định (Pin version) | Ngày phát hành | Ngày hết hỗ trợ (EOL) | Link nguồn chính thức |
|---|---|---|---|---|
| **Node.js (LTS)** | `24.x LTS` | 2025-04-22 (LTS: 2025-10-28) | 2028-04-30 | https://nodejs.org/en/about/previous-releases |
| **pnpm** | `12.14.0` | 2025 | Rolling – chỉ bản mới nhất được vá | https://pnpm.io/ |
| **Next.js** | `16.4.2` | 2025-10-21 (v16) | Rolling – chỉ bản mới nhất được vá | https://nextjs.org/blog |
| **React** | `19.3.1` | 2024-12-05 (v19) | Rolling – chỉ bản mới nhất được vá | https://react.dev/blog |
| **Tailwind CSS** | `4.3.3` | 2025-01-23 (v4) | Rolling – chỉ bản mới nhất được vá | https://tailwindcss.com/blog |
| **shadcn/ui** | `4.22.1` | 2025 | Rolling – chỉ bản mới nhất được vá | https://ui.shadcn.com/docs/changelog |
| **Python** | `3.12.x` | 2023-10-02 | 2028-10-31 | https://devguide.python.org/versions/ |
| **FastAPI** | `0.150.0` | 2024-09 | Rolling – chỉ bản mới nhất được vá | https://fastapi.tiangolo.com/release-notes/ |
| **SQLAlchemy** | `2.1.5` | 2023-01 (v2.0) | Rolling – chỉ bản mới nhất được vá | https://www.sqlalchemy.org/download.html |
| **Alembic** | `1.20.0` | 2024 | Rolling – chỉ bản mới nhất được vá | https://alembic.sqlalchemy.org/ |
| **Pydantic** | `2.14.1` | 2024 | Rolling – chỉ bản mới nhất được vá | https://docs.pydantic.dev/latest/changelog/ |
| **Celery** | `5.6.3` | 2024 | Rolling – chỉ bản mới nhất được vá | https://docs.celeryq.dev/en/stable/history/ |
| **Valkey** (thay thế Redis) | `9.1.x` | 2025 | Rolling – chỉ bản mới nhất được vá | https://valkey.io/ |
| **PostgreSQL** | `17.x` | 2024-09-26 | 2029-11-08 | https://www.postgresql.org/support/versioning/ |
| **Playwright** | `1.64.1` | 2024 | Rolling – chỉ bản mới nhất được vá | https://playwright.dev/ |

---

## 3. Phân tích chi tiết và Lựa chọn chuyên biệt

### 3.1. Frontend Web App & CMS: Next.js 16.4.2 + Tailwind CSS 4.3.3 + shadcn/ui
- **Next.js 16.4.2 & React 19.3.1:** Next.js 14 đã kết thúc hỗ trợ vào 26/10/2025, Next.js 15 kết thúc hỗ trợ vào 21/10/2026. Chọn Next.js 16.x bản vá ổn định mới nhất kết hợp React 19. Kiến trúc Server Components mặc định giúp tối ưu hóa xử lý bảo mật cho phiên làm việc không cần lưu trữ token ở trình duyệt.
- **Tailwind CSS 4.3.3:** Sử dụng engine Oxide viết bằng Rust, cấu hình trực tiếp qua CSS variables trong `globals.css` (cú pháp `@theme`), tốc độ biên dịch nhanh hơn đáng kể so với bản v3.
- **shadcn/ui 4.22.1:** Các component primitives chuẩn hóa từ Radix UI / Base UI hỗ trợ Tailwind v4. Toàn bộ mã nguồn component nằm trong repo (`components/ui/`), tuân thủ design token tại [pace-design-system](../../.agents/skills/pace-design-system/SKILL.md).

### 3.2. Caching & Message Broker: Chuyển từ Redis sang Valkey 9.1.x
- **Lý do pháp lý và bản quyền:** Từ tháng 03/2024, Redis Ltd. đã hủy bỏ bản quyền nguồn mở tự do (BSD-3-Clause) từ bản Redis 7.4, chuyển sang dual-license RSALv2 / SSPLv1. Đến Redis 8, Redis Ltd. bổ sung giấy phép AGPLv3. Tuy nhiên, AGPLv3 là giấy phép strong-copyleft với điều khoản Network Copyleft nghiêm ngặt (buộc phải cung cấp toàn bộ mã nguồn khi cung cấp dịch vụ mạng), gây rủi ro pháp lý và tuân thủ lớn cho hệ thống nội bộ doanh nghiệp.
- **Giải pháp Valkey 9.1.x:** Valkey là dự án fork mã nguồn mở phi lợi nhuận được bảo trợ bởi Linux Foundation (với sự đóng góp của AWS, Google, Microsoft, Ericsson...). Valkey:
  - Duy trì giấy phép **BSD-3-Clause** thuần túy, an toàn cho doanh nghiệp.
  - Tương thích 100% (drop-in replacement) với Redis protocol và các thư viện `redis-py`, Celery broker mà không cần thay đổi logic ứng dụng.

### 3.3. Hệ quản trị cơ sở dữ liệu: Lý do giữ PostgreSQL 17.x dù PostgreSQL 18 đã GA
PostgreSQL 18 hiện tại đã đạt trạng thái GA (General Availability). Tuy nhiên, dự án vẫn quyết định chuẩn hóa trên **PostgreSQL 17.x** vì các lý do kỹ thuật sau:
1. **Thời hạn hỗ trợ dài hạn:** PostgreSQL 17 có EOL chính thức đến **08/11/2029**, vượt xa mốc yêu cầu tối thiểu 31/03/2027 hơn 2,5 năm.
2. **Độ ổn định đã được kiểm chứng (Battle-tested):** PG 17 đã trải qua thời gian vận hành thực tế trong môi trường doanh nghiệp; các extension bắt buộc (`pgcrypto`), image container chuẩn và driver client (`asyncpg`, `psycopg`) hoàn toàn ổn định trên Ubuntu 24.04 LTS.
3. **Giảm thiểu rủi ro trong giai đoạn Pilot (15 tuần):** Tránh các lỗi hồi quy hoặc tương thích chưa được phát hiện ở các bản phát hành đầu tiên của bản major mới (PG 18).
4. **Tính năng đáp ứng toàn diện:** PG 17 sở hữu cơ chế VACUUM thế hệ mới tiết kiệm bộ nhớ RAM tới 20 lần, hỗ trợ hàm `JSON_TABLE` và xử lý JSON chuẩn SQL:2023, đáp ứng tốt schema `DailyBrief` và bảng `audit_events`.

---

## 4. Kiến trúc xác thực & Luồng đăng nhập (BFF Pattern tại FastAPI)

Tuân thủ nguyên tắc phân quyền và an toàn thông tin tại [10-security.md](../../.agents/rules/10-security.md):

### 4.1. Nguyên tắc cốt lõi:
1. **FastAPI đóng vai trò Backend-for-Frontend (BFF) độc quyền xử lý Auth:** Toàn bộ quá trình bắt tay OIDC với Microsoft Entra ID (PKCE, đổi mã authorization code lấy tokens) diễn ra hoàn toàn tại backend FastAPI.
2. **Next.js không lưu trữ Access Token:** Trình duyệt và Next.js Client Components **không lưu trữ** Access Token hoặc ID Token của Entra ID trong `localStorage` hay `sessionStorage`.
3. **Không dùng thư viện Auth lưu token phía client:** Không sử dụng các thư viện như `msal-browser` hay NextAuth lưu JWT ở client.
4. **Session Cookie có cờ bảo vệ:** Trình duyệt chỉ nhận và lưu Server-Side Session Cookie với các thuộc tính:
   - `HttpOnly`: JavaScript phía trình duyệt không thể truy cập (phòng chống rủi ro XSS đánh cắp session).
   - `Secure`: Chỉ truyền qua giao thức HTTPS.
   - `SameSite=Lax`: Phòng chống tấn công CSRF.
   - `Path=/`.
5. **Cùng Origin & Forward Cookie từ Next.js Server:**
   - Reverse proxy (Traefik / Nginx) định tuyến `/api/*` về FastAPI và `/*` về Next.js web trên cùng một domain.
   - Khi Next.js Server Components hoặc Route Handlers gọi API nội bộ sang FastAPI, server Next.js đọc cookie từ request header (`cookies()`) và chuyển tiếp (forward) nguyên vẹn header `Cookie: pace_session=...` sang FastAPI để xác thực người dùng.
6. **Thu hồi Session khi offboard (Revocation):**
   - Khi nhân viên offboard hoặc bị vô hiệu hóa tài khoản trong Microsoft Entra ID / admin thu hồi quyền qua CMS: FastAPI cung cấp API thu hồi ngay lập tức, xóa session key trong Valkey và đánh dấu `revoked_at` trong bảng `user_sessions` (PostgreSQL), đồng thời ghi log vào `audit_events`.
   - Mọi request mang session cookie đã thu hồi sẽ nhận mã lỗi `401 UNAUTHORIZED`.
7. **Lưu trữ phiên bền vững bằng Valkey AOF:**
   - Cấu hình Valkey bật cơ chế lưu trữ AOF (Append-Only File) với chính sách `appendfsync everysec` cho dữ liệu session và PKCE state, đảm bảo phiên đăng nhập của người dùng không bị mất khi container khởi động lại.
8. **Bảo vệ CSRF:** Các request thay đổi trạng thái (POST, PUT, DELETE, PATCH) yêu cầu Anti-CSRF token hoặc custom header (`X-Requested-With: XMLHttpRequest` / `X-CSRF-Token`).

### 4.2. Sơ đồ tuần tự luồng đăng nhập (OIDC + Session Flow):

```mermaid
sequenceDiagram
    autonumber
    actor User as Người dùng (Browser)
    participant Web as Next.js Web App (apps/web)
    participant Proxy as Reverse Proxy (Traefik/Nginx)
    participant API as FastAPI BFF (apps/api)
    participant DB as Postgres & Valkey AOF
    participant Entra as Microsoft Entra ID (OIDC)

    User->>Web: 1. Bấm "Đăng nhập với Microsoft"
    Web->>Proxy: 2. Điều hướng GET /api/v1/auth/login
    Proxy->>API: Chuyển tiếp tới FastAPI
    API->>API: 3. Tạo code_verifier, code_challenge (PKCE), state, nonce
    API->>DB: 4. Lưu tạm PKCE state vào Valkey AOF (TTL 5 phút)
    API-->>User: 5. 302 Redirect tới login.microsoftonline.com
    User->>Entra: 6. Đăng nhập & đồng ý quyền (SSO PACE)
    Entra-->>User: 7. 302 Redirect về /api/v1/auth/callback?code=...&state=...
    User->>Proxy: 8. GET /api/v1/auth/callback?code=...&state=...
    Proxy->>API: Chuyển tiếp tới FastAPI
    API->>DB: 9. Kiểm tra & xác thực state từ Valkey AOF
    API->>Entra: 10. POST /token (back-channel: đổi code + code_verifier)
    Entra-->>API: 11. Trả về id_token, access_token (server-side only)
    API->>DB: 12. Xác thực user/workspace trong PostgreSQL, tạo session_token trong Valkey AOF
    API-->>User: 13. Set-Cookie: pace_session=<session_token>; HttpOnly; Secure; SameSite=Lax
    API-->>User: 14. 302 Redirect về trang chủ (/)
    User->>Web: 15. Truy cập giao diện (Cookie tự động đính kèm)
    Web->>Proxy: 16. Server Component forward Cookie qua GET /api/v1/users/me
    Proxy->>API: Chuyển tiếp request cùng origin
    API->>DB: 17. Tra cứu session trong Valkey, kiểm tra cờ revoked, nạp RBAC
    API-->>Web: 18. Trả về thông tin user & quyền hạn (JSON)
```

---

## 5. Rủi ro & Cách nâng cấp cho từng thành phần (Risks & Upgrade Strategy)

| Thành phần | Rủi ro tiềm ẩn | Chiến lược & Cách thức nâng cấp |
|---|---|---|
| **Node.js 24 LTS** | Thay đổi một số native API khi nâng cấp minor. | Node 24 hỗ trợ đến 04/2028. Cập nhật qua bản vá minor của Docker image `node:24-alpine` và kiểm thử CI. |
| **pnpm 12.14.0** | Thay đổi format lockfile. | Chạy cập nhật lockfile trong PR riêng, kiểm thử `pnpm install --frozen-lockfile` trên CI. |
| **Next.js 16.4.2 & React 19.3.1** | Thay đổi trong các Server Actions hoặc Request APIs. | Khóa version cụ thể trong `package.json`. Ưu tiên Server Components, tách biệt rõ ràng các interactive components bằng `"use client"`. |
| **Tailwind CSS 4.3.3 & shadcn/ui** | Một số thư viện ngoài chưa tương thích hoàn toàn với engine CSS-first v4. | Cấu hình theme trực tiếp qua CSS variables tại `app/globals.css`. Mã nguồn shadcn/ui lưu nội bộ nên dễ kiểm soát và tùy chỉnh. |
| **Python 3.12 & FastAPI 0.150.0** | Deprecation các package phụ thuộc liên quan đến asyncio. | Sử dụng `uv` quản lý lockfile `uv.lock`. Kiểm thử tự động với `pytest` và `mypy --strict`. |
| **SQLAlchemy 2.1.5 & Alembic 1.20.0** | Xung đột locking transaction khi migrate database đang chạy. | Áp dụng nguyên tắc Expand/Contract cho database migrations: mọi migration đều có hàm `downgrade()`, kiểm thử up $\rightarrow$ down $\rightarrow$ up trên testcontainers Postgres thật trước khi merge. |
| **Pydantic 2.14.1** | Thay đổi nhỏ trong schema serialization. | Tận dụng Rust core của Pydantic v2. Schema validation cho `DailyBrief` được bọc try/except và ghi log chi tiết khi có sai lệch. |
| **Celery 5.6.3 & Valkey 9.1.x** | Task bị timeout hoặc mất kết nối broker khi VM khởi động lại. | Valkey bật AOF persistence (`appendfsync everysec`). Celery cấu hình `acks_late=True`, `task_reject_on_worker_lost=True`, giới hạn retry có jitter và định tuyến lỗi sang Dead-Letter Queue (DLQ). |
| **PostgreSQL 17.x** | Quản lý dung lượng lưu trữ trên VM. | Phiên bản 17 hỗ trợ tới tháng 11/2029. Định kỳ chạy vacuum định kỳ và backup tự động bằng `pg_dump` theo runbook. |
| **Playwright 1.64.1** | Browser binaries thay đổi hoặc flaky test do độ trễ mạng. | Cố định phiên bản; cache browser binaries trên CI; viết kịch bản kiểm thử dựa trên ngữ nghĩa (`getByRole`, `getByTestId`). |

---

## 6. Chính sách cập nhật bản vá (Patching & Dependency Policy)

Để đảm bảo hệ thống luôn được bảo vệ khỏi các lỗ hổng bảo mật (CVE) mà không gây gián đoạn tính ổn định:

1. **Cấu hình công cụ tự động:**
   - Sử dụng **Dependabot** tích hợp trên GitHub repository.
   - Bật **GitHub Secret Scanning** và **Push Protection** (ADR-015).
2. **Tần suất quét và kiểm tra:**
   - Quét định kỳ hàng tuần (**Weekly vào thứ Hai lúc 08:00 Asia/Ho_Chi_Minh**).
3. **Quy trình xử lý PR phụ thuộc:**
   - **Patch updates (x.y.Z $\rightarrow$ x.y.Z+1):** Dependabot tự động mở PR. GitHub Actions chạy toàn bộ test matrix (lint, typecheck, pytest, playwright e2e). Nếu tất cả test xanh và không có cảnh báo bảo mật, PR được phép merge sau khi được phê duyệt.
   - **Minor updates (x.Y.z $\rightarrow$ x.Y+1.0):** Yêu cầu kiểm tra kỹ changelog, chạy test thủ công và staging trước khi merge.
   - **Major updates (X.y.z $\rightarrow$ X+1.0.0):** Không tự động merge; chỉ thực hiện theo kế hoạch nâng cấp riêng được phê duyệt bằng ADR.
4. **Quy trình khẩn cấp với lỗ hổng nghiêm trọng (Critical/High CVE):**
   - Khi có cảnh báo bảo mật CVE mức High/Critical từ GitHub Dependabot Alerts, đội dự án kích hoạt quy trình nóng: kiểm tra PoC, cập nhật bản vá và triển khai lại lên VM trong vòng **24 giờ**.

---

## 7. Consequences (Hệ quả và tác động)

### 7.1. Tác động tích cực
- **Đáp ứng tiêu chí vòng đời EOL:** Các nền tảng chính (Node.js 24 LTS, Python 3.12, PostgreSQL 17) đều có thời hạn hỗ trợ chính thức tối thiểu đến tháng 04/2028 và tháng 11/2029.
- **An toàn pháp lý doanh nghiệp:** Loại bỏ rủi ro bản quyền của Redis 7.4+ và Redis 8 (AGPLv3) bằng cách chuẩn hóa trên Valkey 9.1.x (Linux Foundation, BSD-3-Clause).
- **Phân tách an toàn luồng dữ liệu:** Mô hình BFF tại FastAPI giúp kiểm soát phiên làm việc tập trung; token không xuất hiện ở client JavaScript.
- **Hiệu năng và giao diện hiện đại:** Next.js 16 và Tailwind CSS v4 cung cấp nền tảng giao diện chuẩn hóa theo [pace-design-system](../../.agents/skills/pace-design-system/SKILL.md).

### 7.2. Việc cần làm tiếp theo
1. Trình Chủ dự án phê duyệt chính thức (chuyển sang `Accepted`).
2. Cập nhật [traceability.md](../traceability.md).
3. Khởi tạo cấu trúc monorepo trong Phase 1 (story **INF-01a**) với các phiên bản đã chỉ định.