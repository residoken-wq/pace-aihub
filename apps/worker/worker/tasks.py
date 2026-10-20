from worker.celery_app import app


@app.task(name="worker.tasks.ping")  # type: ignore[untyped-decorator]
def ping() -> str:
    """Liveness task: proves the broker round-trip works."""
    return "pong"
