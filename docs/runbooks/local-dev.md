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
```
- Mailpit (fake SMTP): http://localhost:8025. Không có email nào ra ngoài máy.
- Mọi cổng chỉ bind `127.0.0.1`.
- `POSTGRES_PASSWORD` chỉ dùng ký tự chữ, số, `-`, `_` vì được ghép vào URL kết nối.
- Dừng: `pnpm dev:down`. Xoá cả dữ liệu: thêm `-v` (mất dữ liệu dev).

## Chạy API / worker ngoài Docker (khi đang code)
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
```

## Kiểm tra trước khi mở PR
```bash
cd apps/api    && uv run ruff format --check . && uv run ruff check . && uv run mypy && uv run pytest -q
cd apps/worker && uv run ruff format --check . && uv run ruff check . && uv run mypy && uv run pytest -q
pnpm contracts:gen && git diff --exit-code packages/contracts   # contracts phải khớp code
```
Test có marker `integration` dùng testcontainers (Postgres 17, Valkey 9.1). Không có Docker thì tự skip; CI luôn chạy chúng.

## Sự cố thường gặp
- `/readyz` trả 503: xem trường `checks` để biết Postgres hay Valkey đang `down`. Log API ghi `readiness_check_failed` kèm loại lỗi, không ghi chuỗi kết nối.
- `pnpm` báo sai phiên bản: chạy `corepack enable` để dùng đúng bản trong `packageManager`.
