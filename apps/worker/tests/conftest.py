import os

# Settings are read at import time of worker.celery_app; give them inert values.
os.environ.setdefault("PACE_DATABASE_URL", "postgresql+asyncpg://unused/unused")
os.environ.setdefault("PACE_VALKEY_URL", "redis://valkey.invalid:6379/0")
