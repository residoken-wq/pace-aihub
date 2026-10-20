# Build from repo root: docker build -f apps/worker/Dockerfile .
FROM python:3.12.15-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PROJECT_ENVIRONMENT=/opt/venv \
    PATH="/opt/venv/bin:$PATH"

RUN pip install --no-cache-dir uv==0.13.3 \
    && useradd --create-home --uid 10001 pace

# The worker depends on ../api (shared settings/models), so both trees are copied.
COPY apps/api/ /srv/apps/api/
WORKDIR /srv/apps/worker
COPY apps/worker/ ./
RUN uv sync --frozen --no-dev

USER pace
CMD ["celery", "-A", "worker.celery_app", "worker", "-Q", "collect,analyze,dispatch,reconcile,dlq", "--loglevel=INFO"]
