---
trigger: glob
globs: apps/api/migrations/**, apps/api/app/models/**, **/*.sql
---
# Database rules (PostgreSQL 15+)

- Baseline schema = `docs/specs/03_DATABASE_SCHEMA.sql`. Changes ONLY via Alembic migrations; never edit an applied migration.
- Every migration: reversible `downgrade`, tested up→down→up in CI against real Postgres.
- Money `numeric(18,6)`; timestamps `timestamptz`; ids `uuid` (`gen_random_uuid()`); enums as Postgres ENUM per spec.
- Tenant tables carry `workspace_id`; add composite indexes starting with `workspace_id`.
- Keep uniqueness guarantees: `runs(tool_id, idempotency_key)`, partial unique `runs(tool_id, schedule_slot)`, `budget_reservations(run_id)`, `deliveries(idempotency_key)`, `reports(run_id, revision)`.
- Approved reports are immutable: regenerate = new revision row.
- Destructive changes (drop/rename column, type narrowing) require an expand→migrate→contract plan and user confirmation.
- Use the `pace-db-migration` skill for any schema change.
