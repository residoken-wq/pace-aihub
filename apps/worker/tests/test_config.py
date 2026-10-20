from worker import config
from worker.celery_app import app


def test_pipeline_queues_and_dlq_declared() -> None:
    names = {q.name for q in app.conf.task_queues}
    assert names == {"collect", "analyze", "dispatch", "reconcile", "dlq"}


def test_reliability_settings() -> None:
    assert app.conf.task_acks_late is True
    assert app.conf.task_reject_on_worker_lost is True
    assert app.conf.worker_prefetch_multiplier == 1
    assert app.conf.broker_transport_options["visibility_timeout"] >= 600
    assert app.conf.accept_content == ["json"]


def test_ping_routed_to_reconcile_queue() -> None:
    assert config.task_routes["worker.tasks.ping"]["queue"] == "reconcile"
    app.loader.import_default_modules()  # what a worker does on start (`include=`)
    assert "worker.tasks.ping" in app.tasks
