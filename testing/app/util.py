import redis
def redis_client():
    from .conf import REDIS_HOST, REDIS_PORT, REDIS_DB
    return redis.StrictRedis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        db=REDIS_DB
    )
