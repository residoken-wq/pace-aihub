import shutil
import subprocess
from collections.abc import Iterator
from contextlib import contextmanager

# Keep in sync with infra/docker-compose.dev.yml and ADR-013.
POSTGRES_IMAGE = "postgres:17.11-alpine"
VALKEY_IMAGE = "valkey/valkey:9.1.2-alpine"


def docker_available() -> bool:
    docker = shutil.which("docker")
    if docker is None:
        return False
    return subprocess.run([docker, "info"], capture_output=True, check=False).returncode == 0  # noqa: S603


@contextmanager
def valkey_url() -> Iterator[str]:
    """Start a throwaway Valkey and yield its redis:// URL."""
    from testcontainers.core.container import DockerContainer
    from testcontainers.core.waiting_utils import wait_for_logs

    with DockerContainer(VALKEY_IMAGE).with_exposed_ports(6379) as vk:
        wait_for_logs(vk, "Ready to accept connections")
        yield f"redis://{vk.get_container_host_ip()}:{vk.get_exposed_port(6379)}/0"
