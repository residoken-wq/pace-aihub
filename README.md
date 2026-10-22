# PACE AI Hub

Nền tảng nội bộ để tạo, chạy, chia sẻ và quản trị AI Workflows theo Personal / Team / Organization.
Nguyên tắc: *share spending capacity, never share the key*.

- Bối cảnh và quy tắc: [`AGENTS.md`](AGENTS.md), [`docs/HANDOFF.md`](docs/HANDOFF.md)
- Spec: [`docs/specs/`](docs/specs/), quyết định: [`docs/adr/`](docs/adr/), kế hoạch: [`docs/plan/PHASES.md`](docs/plan/PHASES.md)
- Chạy local: [`docs/runbooks/local-dev.md`](docs/runbooks/local-dev.md)

## Cấu trúc
```
apps/api            FastAPI (Python 3.12), Alembic
apps/worker         Celery trên Valkey
apps/web            Next.js 16, Tailwind v4
packages/contracts  OpenAPI + JSON Schema + TS types sinh tự động
infra/              docker-compose dev
```

## Giấy phép
Proprietary, xem [`LICENSE`](LICENSE). Repo đang để public tạm thời (ADR-015), nhưng điều đó không cấp quyền sử dụng hay sao chép.
