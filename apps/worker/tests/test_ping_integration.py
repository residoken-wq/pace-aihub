import shutil
import subprocess

import pytest

VALKEY_IMAGE = "valkey/valkey:9.1.2-alpine"  # keep in sync with infra/docker-compose.dev.yml


def _docker_available() -> bool:
    docker = shutil.which("docker")
    if docker is None:
        return False
    return subprocess.run([docker, "info"], capture_output=True, check=False).returncode == 0  # noqa: S603


pytestmark = [
    pytest.mark.integration,
    pytest.mark.skipif(not _docker_available(), reason="Docker not available"),
]


def test_ping_round_trip_through_valkey() -> None:
    from celery.contrib.testing.worker import start_worker
    from testcontainers.core.container import DockerContainer
    from testcontainers.core.waiting_utils import wait_for_logs

    from worker.celery_app import app
    from worker.tasks import ping

    with DockerContainer(VALKEY_IMAGE).with_exposed_ports(6379) as vk:
        wait_for_logs(vk, "Ready to accept connections")
        url = f"redis://{vk.get_container_host_ip()}:{vk.get_exposed_port(6379)}/0"
        app.conf.broker_url = url
        app.conf.result_backend = url
        with start_worker(app, queues=["reconcile"], perform_ping_check=False):
            assert ping.delay().get(timeout=10) == "pong"
