# ADR-013: Chuẩn hoá Tech Stack và phiên bản cho PACE AI Hub
- **Status:** Proposed
- **Date:** 2026-10-20 · **Deciders:** Tech Lead, Chủ dự án, IT Platform Lead, BA-PO · **Story:** INF-01a, DB-01, UI-00

---

## 1. Context (Bối cảnh)
Theo `01_PRD.md`, `02_SYSTEM_ARCHITECTURE.md`, `AGENTS.md` và `docs/plan/PHASES.md`, PACE AI Hub là nền tảng quản trị AI workflow tập trung dành cho nội bộ PACE. Hệ thống yêu cầu:
- Tự phục vụ an toàn (self-service AI Tool Catalog), chia sẻ ngân sách chi tiêu thay vì chia sẻ Claude API key.
- Phân quyền nghiêm ngặt theo workspace (Personal, Team, Org), chống rò rỉ dữ liệu chéo (IDOR) và bảo đảm tính toàn vẹn kiểm toán (Audit).
- Kiến trúc monorepo phân tách rõ giữa giao diện người dùng/CMS quản trị, API điều phối & quản trị ngân sách, và tiến trình worker chạy nền (thu thập tin, sinh báo cáo qua Claude Gateway, dispatch email).
- Tuân thủ các quyết định đã phê duyệt trong `docs/adr/ADR-009-015-decisions.md`:
  - **ADR-009:** CI/CD bằng GitHub Actions (build, test, push image lên GHCR).
  - **ADR-010:** Môi trường Pilot chạy trên VM nội bộ riêng biệt (Ubuntu 24.04 LTS), triển khai dạng pull-based container qua Docker Compose, cô lập egress mạng.
  - **ADR-011:** Đội ngũ tinh gọn 4 người (Tech Lead/BE, FE/UI, Fullstack/DevOps-Sec, BA-PO/QA Lead), năng lực tập trung đòi hỏi công nghệ phải có hệ sinh thái trưởng thành, ít cấu hình rườm rà.
  - **ADR-012:** Hỗ trợ Antigravity hỗ trợ lập trình với nguyên tắc không lưu trữ secret hay PII thật trong mã nguồn/prompt.
  - **ADR-014:** Đưa CMS-01 và UI-00 vào phạm vi P0 (đòi hỏi Design System và giao diện quản trị ngân sách/quota phải đồng bộ ngay từ đầu).
  - **ADR-015:** Repo GitHub tạm thời để public, kiểm soát tuyệt đối secret qua biến môi trường/vault, loại trừ toàn bộ dữ liệu nội bộ/private.

Để đảm bảo tiến độ triển khai walking skeleton trong 48 giờ sau khi nhận VM (theo cam kết IT tại ADR-010) và sẵn sàng cho Phase 1, đội dự án cần chốt bộ Tech Stack với các phiên bản ổn định hiện hành (LTS / Stable), hạn chế tối đa rủi ro xung đột phụ thuộc và lỗi tương thích.

---

## 2. Options considered (Các phương án xem xét)

### 2.1. Frontend Web App & CMS
| Tiêu chí | Phương án A (Đề xuất): Next.js 14.2 LTS (App Router, TS, Tailwind, shadcn/ui) | Phương án B: Next.js 15 + React 19 (Mới phát hành) | Phương án C: Vite + React SPA |
|---|---|---|---|
| **Ưu điểm** | - Ổn định cao nhất với React 18, tương thích 100% với toàn bộ hệ sinh thái shadcn/ui & Radix UI.<br>- App Router hỗ trợ Server Components, bảo vệ logic OIDC session cookie.<br>- Build nhanh, tài liệu phong phú, agent sinh code chính xác. | - Tiếp cận các tính năng mới nhất của Next.js 15 và React 19. | - Đơn giản, thuần SPA, không cần Node runtime trên server. |
| **Nhược điểm** | - Không có một số cải tiến nhỏ về cache và Async Request APIs của bản 15. | - Rủi ro tương thích với các component của shadcn/ui, một số thư viện React 18 chưa hỗ trợ React 19 peer dependencies, có thể gây chậm tiến độ. | - Khó xử lý HttpOnly session cookies an toàn và SSR/SEO nội bộ; tách rời BFF. |
| **Kết luận** | **Chọn Phương án A** (Next.js 14.2.x LTS). | Loại (quá mới cho dự án 15 tuần). | Loại (không đạt chuẩn bảo mật session). |

### 2.2. Backend API & Core Logic
| Tiêu chí | Phương án A (Đề xuất): Python 3.12 + FastAPI 0.115 + SQLAlchemy 2.0 (Async) + Pydantic v2 | Phương án B: Node.js (NestJS / Express) |
|---|---|---|
| **Ưu điểm** | - Chuẩn hóa theo `AGENTS.md` và `02_SYSTEM_ARCHITECTURE.md`.<br>- Pydantic v2 có hiệu năng cao (Rust core), sinh JSON Schema và kiểm thực DailyBrief JSON Schema chính xác.<br>- Xử lý tính toán tiền tệ `Decimal` và thư viện AI (Anthropic SDK, tokenizers) tốt nhất.<br>- Quản lý gói bằng `uv` siêu tốc và tin cậy. | - Chia sẻ TypeScript types giữa Web và API. |
| **Nhược điểm** | - Hai ngôn ngữ (TS ở frontend, Python ở backend), cần `packages/contracts` để sinh TypeScript client từ OpenAPI. | - Hệ sinh thái AI, xử lý data/cào tin và thư viện LLM trong Node.js kém linh hoạt hơn Python; xử lý tác vụ nền nặng tốn tài nguyên hơn. |
| **Kết luận** | **Chọn Phương án A** (FastAPI + Python 3.12). | Loại. |

### 2.3. Background Worker & Task Queue
| Tiêu chí | Phương án A (Đề xuất): Celery 5.4 + Redis 7.2 | Phương án B: ARQ / SAQ (Asyncio Redis Queue) | Phương án C: Power Automate Cloud Flow |
|---|---|---|
| **Ưu điểm** | - Hệ sinh thái hoàn chỉnh nhất Python; hỗ trợ Celery Beat (scheduler chuẩn cho cron 08:30 Asia/Ho_Chi_Minh).<br>- Tích hợp sẵn cơ chế retry, rate limit, dead-letter queue (DLQ), task acknowledgment.<br>- Chạy bền vững trong Docker container trên VM nội bộ (ADR-010). | - Nhẹ, hỗ trợ asyncio gốc của Python. | - Có sẵn trong tenant Microsoft 365 của PACE. |
| **Nhược điểm** | - Cần cấu hình serialization JSON an toàn; nặng hơn asyncio queue đơn giản. | - Thiếu hệ thống quản trị scheduler phong phú như Celery Beat; cộng đồng nhỏ hơn. | - Rủi ro chi phí Premium Connector (ADR-005); khó kiểm soát mã nguồn bằng Git và CI/CD; không đáp ứng UAT-03/09. |
| **Kết luận** | **Chọn Phương án A** (Celery 5.4 + Redis 7.2). | Loại. | Loại khỏi lõi (chỉ dùng kết nối SharePoint/Outlook khi được cấp phép). |

### 2.4. Database & Persistence
| Tiêu chí | Phương án A (Đề xuất): PostgreSQL 16 | Phương án B: PostgreSQL 15 |
|---|---|---|
| **Ưu điểm** | - Hỗ trợ đầy đủ extension `pgcrypto` theo `03_DATABASE_SCHEMA.sql`.<br>- Tối ưu hóa truy vấn JSONB, cải thiện hiệu năng partitioning cho bảng `audit_events`.<br>- Hỗ trợ các câu lệnh locking `SELECT ... FOR UPDATE` phục vụ atomic budget reservation (GW-02).<br>- Phiên bản ổn định mặc định trên Ubuntu 24.04 LTS (ADR-010). | - Đáp ứng yêu cầu tối thiểu trong `03_DATABASE_SCHEMA.sql` (ghi PostgreSQL 15+). |
| **Nhược điểm** | - Không có. | - Cũ hơn bản mặc định trên Ubuntu 24.04. |
| **Kết luận** | **Chọn Phương án A** (PostgreSQL 16). | Bản dự phòng nếu IT yêu cầu cụ thể. |

---

## 3. Decision (Quyết định Tech Stack chuẩn hóa)

Chốt danh mục công nghệ và phiên bản cố định cho toàn bộ dự án:

### 3.1. Phân tầng ứng dụng
1. **Frontend (`apps/web`):**
   - **Framework:** Next.js `14.2.x` (App Router, React 18, TypeScript 5.x).
   - **Styling & UI:** Tailwind CSS `v3.4.x`, `shadcn/ui` (Radix UI primitives, `lucide-react`, `class-variance-authority`).
   - **Form & Validation:** `react-hook-form`, `zod`.
   - **State & Data Fetching:** TanStack Query (React Query) `v5.x` kết hợp fetcher được sinh từ OpenAPI.
   - **i18n:** Giao diện hỗ trợ song ngữ với tiếng Việt mặc định (i18n dictionary hoặc `next-intl`).

2. **Backend API (`apps/api`):**
   - **Ngôn ngữ & Runtime:** Python `3.12.x`.
   - **Web Framework:** FastAPI `0.115.x` (Uvicorn ASGI server).
   - **ORM & DB Access:** SQLAlchemy `2.0.x` (hỗ trợ async engine `asyncpg` cho web queries và sync engine `psycopg` cho worker transactions khi cần).
   - **Data Schema & Serialization:** Pydantic `v2.x` và Pydantic Settings.
   - **Database Migration:** Alembic `1.13.x`.
   - **AI Integration:** Anthropic Python SDK (`anthropic >= 0.36.x`) tích hợp trong Claude API Gateway với `Decimal` cho toàn bộ tính toán chi phí và quota.
   - **HTTP Client (Collector & Graph):** `httpx` (hỗ trợ timeout nghiêm ngặt, DNS rebinding checks, chặn RFC1918/metadata IP theo `10-security.md`).

3. **Background Worker & Scheduler (`apps/worker`):**
   - **Task Queue:** Celery `5.4.x` kết hợp `celery[redis]`.
   - **Scheduler:** Celery Beat (lập lịch theo múi giờ `Asia/Ho_Chi_Minh` bằng `pytz` / `zoneinfo`).
   - **Broker & Results:** Redis `7.2.x` (hoặc `7.4.x`), kích hoạt cơ chế lưu trữ bền vững RDB/AOF.

4. **Database & Storage:**
   - **RDBMS:** PostgreSQL `16.x` với extension `pgcrypto`.
   - **Data Types:** Chuẩn hóa kiểu tiền tệ `numeric(18,6)` / Python `Decimal`, thời gian lưu UTC `timestamptz`, JSON dạng `jsonb`.

5. **Contracts & Code Generation (`packages/contracts`):**
   - Single source of truth cho API contracts và Daily Brief schema:
     - OpenAPI `3.1` sinh từ FastAPI endpoint metadata.
     - JSON Schema cho DailyBrief (`daily_brief.schema.json`).
     - Tool sinh TS client: `openapi-typescript-codegen` hoặc `orval`.

6. **DevOps & Môi trường triển khai:**
   - **Quản lý gói:**
     - Frontend / Root monorepo: `pnpm 9.x`.
     - Python (API & Worker): `uv 0.4.x` (nhanh hơn pip-tools, khóa lockfile bằng `uv.lock`).
   - **Container:** Docker Engine `27.x`, Docker Compose `v2.29+`.
   - **OS Host (Pilot VM):** Ubuntu `24.04 LTS` (ADR-010).
   - **Reverse Proxy / TLS:** Traefik `v3` hoặc NGINX `1.26` (tự động renew TLS hoặc load chứng chỉ nội bộ IT cấp).
   - **CI/CD:** GitHub Actions (ADR-009) build multi-stage Docker images đẩy lên GitHub Container Registry (GHCR).

---

## 4. Consequences (Hệ quả và tác động)

### 4.1. Tác động tích cực
- Đồng bộ tuyệt đối giữa các văn bản kiến trúc (`AGENTS.md`, `02_SYSTEM_ARCHITECTURE.md`, `PHASES.md`).
- Tốc độ phát triển tối ưu: `uv` giúp cài đặt môi trường Python trong vài giây; Next.js 14.2 và shadcn/ui loại bỏ xung đột phiên bản React 19.
- Đáp ứng cam kết triển khai walking skeleton lên VM nội bộ trong vòng 48 giờ sau khi IT bàn giao (Phase 1 / INF-01c).
- Kiểm soát chi phí và rủi ro rò rỉ bảo mật: Gateway độc quyền gọi Anthropic API, toàn bộ secrets chỉ nằm trong `.env` trên VM hoặc Vault.

### 4.2. Việc cần làm tiếp theo (Action items)
1. Cập nhật `docs/traceability.md` đánh dấu ADR-013 ở trạng thái Proposed.
2. Trình Chủ dự án và Tech Lead phê duyệt chính thức (chuyển sang `Accepted`).
3. Khởi tạo cấu trúc monorepo trong Phase 1 (story `INF-01a`) khớp đúng các phiên bản đã chỉ định trong file `package.json` và `pyproject.toml`.

---

## 5. Revisit trigger (Điều kiện xem xét lại)
- Khi dự án chuyển từ giai đoạn Pilot sang Production quy mô lớn trên Cloud (Azure / AWS) cần Kubernetes hoặc managed services (Azure App Service, Amazon ECS, Managed Postgres).
- Khi hệ sinh thái React 19 và Next.js 15 đạt độ ổn định hoàn toàn và shadcn/ui chuyển sang hỗ trợ chính thức.
- Nếu IT yêu cầu đổi cơ chế task queue sang Azure Service Bus hoặc giải pháp hàng đợi doanh nghiệp khác.