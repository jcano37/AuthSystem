import redis

from app.core.config import settings

redis_url = f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_DB}"
redis_client = redis.from_url(redis_url)


def add_to_blacklist(token: str, expires_in: int) -> None:
    """Add a token to the blacklist with expiration"""
    redis_client.setex(f"blacklist:{token}", expires_in, "1")


def is_blacklisted(token: str) -> bool:
    """Check if a token is blacklisted"""
    return bool(redis_client.get(f"blacklist:{token}"))


def increment_rate_limit(key: str, window: int = 60) -> int:
    """Increment rate limit counter and return current count"""
    pipe = redis_client.pipeline()
    now = redis_client.time()[0]
    window_key = f"ratelimit:{key}:{now // window}"

    pipe.incr(window_key)
    pipe.expire(window_key, window)
    result = pipe.execute()

    return result[0]


def check_rate_limit(key: str, limit: int, window: int = 60) -> bool:
    """Check if rate limit is exceeded"""
    current = increment_rate_limit(key, window)
    return current <= limit
