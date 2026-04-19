import redis
import os

pool = redis.ConnectionPool.from_url(
    os.getenv("REDIS_URL", "redis://localhost:6379"),
    decode_responses=True,
    max_connections=20,  # limit max connections to prevent overload
)

r = redis.Redis(connection_pool=pool)
