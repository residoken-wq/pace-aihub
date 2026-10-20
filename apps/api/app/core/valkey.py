from redis.asyncio import Redis

from app.core.config import Settings


def create_valkey(settings: Settings) -> Redis:
    # Valkey speaks the Redis protocol (ADR-013); redis-py is the client.
    client: Redis = Redis.from_url(settings.valkey_url.get_secret_value())
    return client
