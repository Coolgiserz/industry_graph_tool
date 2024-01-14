import redis
import pickle
class RedisClient(object):
    def __init__(self, host, port, db):
        self.handler = redis.StrictRedis(host=host,port=port, db=db)

    def flushdb(self):
        """
        清理数据库缓存
        """
        print("清理缓存...")
        self.handler.flushdb()

    def set_pkl_object(self, key, obj):
        self.handler.set(key, pickle.dumps(obj))

    def get_pkl_object(self, key):
        res = self.handler.get(key)
        if res is None:
            return None
        else:
            return pickle.loads(res)
