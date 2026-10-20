from kombu import Exchange, Queue

# One queue per pipeline stage, plus a dead-letter queue (20-backend-fastapi.md).
QUEUE_NAMES = ("collect", "analyze", "dispatch", "reconcile", "dlq")

task_queues = tuple(Queue(name, Exchange(name), routing_key=name) for name in QUEUE_NAMES)
task_default_queue = "collect"
task_routes = {"worker.tasks.ping": {"queue": "reconcile"}}

# Reliability (ADR-013 §5): ack after the task finishes and requeue if the worker dies.
task_acks_late = True
task_reject_on_worker_lost = True
worker_prefetch_multiplier = 1
# Unacked messages are redelivered after this many seconds; must exceed the longest task.
broker_transport_options = {"visibility_timeout": 3600}
broker_connection_retry_on_startup = True

task_serializer = "json"
result_serializer = "json"
accept_content = ["json"]
timezone = "UTC"
enable_utc = True
