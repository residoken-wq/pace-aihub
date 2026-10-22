# Runbook: môi trường dev local

## Yêu cầu
- Docker + Docker Compose v2
- Node.js 24 (`.nvmrc`), bật Corepack để dùng đúng pnpm 12 (`corepack enable`)
- [uv](https://docs.astral.sh/uv/) (tự cài Python 3.12 khi chạy `uv sync`)

## Chạy toàn bộ stack bằng Docker
```bash
cp .env.example .env        # điền POSTGRES_USER / POSTGRES_PASSWORD / POSTGRES_DB (giá trị dev tuỳ chọn)
pnpm dev:up                 # = docker compose -f infra/docker-compose.dev.yml --env-file .env up -d --build
docker compose -f infra/docker-compose.dev.yml ps   # tất cả phải "healthy"
curl -s localhost:8000/healthz   # {"status":"ok"}
curl -s localhost:8000/readyz    # {"status":"ready","checks":{"postgres":"ok","valkey":"ok"}}
curl -s localhost:3000/          # Next.js web placeholder
```
- Web App: http://localhost:3000 (hiển thị trạng thái kết nối tới API)
- Mailpit (fake SMTP): http://localhost:8025. Không có email nào ra ngoài máy.
- Mọi cổng chỉ bind `127.0.0.1`.
- `POSTGRES_PASSWORD` chỉ dùng ký tự chữ, số, `-`, `_` vì được ghép vào URL kết nối.
- Dừng: `pnpm dev:down`. Xoá cả dữ liệu: thêm `-v` (mất dữ liệu dev).

## Chạy API / worker / web ngoài Docker (khi đang code)
Cần Postgres và Valkey đang chạy (ví dụ chỉ bật 2 service này: `docker compose -f infra/docker-compose.dev.yml --env-file .env up -d postgres valkey`).
Điền `PACE_DATABASE_URL` và `PACE_VALKEY_URL` trong `.env`, rồi export vào shell.

```bash
cd apps/api
uv sync
uv run alembic upgrade head
uv run uvicorn app.main:create_app --factory --reload

cd apps/worker
uv sync
uv run celery -A worker.celery_app worker -Q collect,analyze,dispatch,reconcile,dlq --loglevel=INFO

cd apps/web
pnpm dev       # http://localhost:3000, kết nối API qua API_INTERNAL_URL (mặc định http://127.0.0.1:8000)
```

## Kiểm tra trước khi mở PR
```bash
cd apps/api    && uv run ruff format --check . && uv run ruff check . && uv run mypy && uv run pytest -q
cd apps/worker && uv run ruff format --check . && uv run ruff check . && uv run mypy && uv run pytest -q
pnpm -C apps/web lint && pnpm -C apps/web typecheck && pnpm -C apps/web test
pnpm contracts:gen && git diff --exit-code packages/contracts   # contracts phải khớp code
```
Playwright e2e cho web (chạy khi stack Docker đang bật):
```bash
pnpm -C apps/web e2e
```
Test có marker `integration` dùng testcontainers (Postgres 17, Valkey 9.1). Không có Docker thì tự skip; CI luôn chạy chúng.

## Pre-commit hook
Repo cấu hình pre-commit kiểm tra format (Ruff), typing (mypy), lint (ESLint) và phát hiện rò rỉ bí mật (Gitleaks).
Chạy kiểm tra thủ công toàn bộ file:
```bash
uvx pre-commit run --all-files
```
Cài đặt hook tự động chạy trước mỗi lệnh `git commit`:
```bash
uvx pre-commit install
```
*(Lưu ý: Prettier chưa có trong dependencies repo, format code web tuân thủ ESLint).*

## Cách đọc kết quả CI trên GitHub Actions
Pipeline CI (`.github/workflows/ci.yml`) chạy tự động trên mỗi Pull Request và mỗi lần push vào `main`:
1. **API Quality & Tests (`api`)**: Kiểm tra ruff check/format, mypy, pytest. Chú ý log pytest phải có **0 skipped** (toàn bộ integration test với Postgres và Valkey containers phải pass).
2. **Worker Quality & Tests (`worker`)**: Tương tự API, kiểm tra celery tasks và Valkey integration tests (**0 skipped**).
3. **Database Migrations (`migrations`)**: Chạy độc lập `alembic upgrade head -> downgrade base -> upgrade head` trên container Postgres sạch để đảm bảo migration có thể rollback an toàn.
4. **API Contracts Sync (`contracts`)**: Chạy `pnpm contracts:gen` và so sánh `git diff`. Nếu có endpoint thay đổi mà quên gen contracts, job này sẽ fail.
5. **Web Quality & Build (`web`)**: Chạy `eslint`, `tsc --noEmit`, Vitest và standalone `next build`.
6. **Security Scans (`security`)**: Quét toàn bộ lịch sử git bằng Gitleaks CLI, kiểm tra CVE với `pnpm audit --prod` và `pip-audit`.
7. **End-to-End Tests (`e2e`)**: Khởi động stack docker compose dev với mật khẩu ngẫu nhiên, chạy Playwright e2e test. Nếu có lỗi, tải artifact `playwright-report` từ trang tóm tắt của Action run để xem trace và screenshot.

## Sự cố thường gặp
- `/readyz` trả 503: xem trường `checks` để biết Postgres hay Valkey đang `down`. Log API ghi `readiness_check_failed` kèm loại lỗi, không ghi chuỗi kết nối.
- `pnpm` báo sai phiên bản: chạy `corepack enable` để dùng đúng bản trong `packageManager`.
- Pre-commit hoặc testcontainers báo lỗi Docker: đảm bảo Docker daemon đang chạy (`docker info`). Trên Windows với WSL2, đảm bảo Docker socket có thể kết nối.
