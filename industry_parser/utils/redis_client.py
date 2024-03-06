import redis
class RedisClient(object):
    def __init__(self):
        self.handler = redis.StrictRedis(host="localhost",port=6379, db=0)

