import logging
from pathlib import Path

from redis.exceptions import RedisError

from app.config import settings
from app.redis_client import redis_client

LUA_SCRIPT_PATH = Path(settings.LUA_FOLDER_PATH) / "token_bucket.lua"

LUA_SCRIPT = Path(LUA_SCRIPT_PATH).read_text()
logger = logging.getLogger(__name__)


class TokenBucketRateLimiter:
    def __init__(self, limit: int, window_size: int):
        self.limit = limit
        self.window_size = window_size

    def allow_request(self, key: str) -> bool:
        try:
            result = redis_client.eval(
                LUA_SCRIPT, 1, key, self.limit, self.window_size
            )
        except RedisError:
            logger.exception("Redis rate limit check failed")
            raise

        return bool(result)


token_bucket_limiter = TokenBucketRateLimiter(
    limit=settings.RATE_LIMIT_CAPACITY, window_size=settings.RATE_LIMIT_WINDOW
)
