import redis


class RedisHandler:

    def __init__(self):
        self.r = None

    def __enter__(self):
        self.r = redis.Redis(connection_pool=redis.ConnectionPool(
            host='localhost', port=6379,
            db=0, decode_responses=True))
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.r.close()

    def add(self, name, value):
        self.r.sadd(name, value)

    def set(self, name, value, ex=None):
        if ex:
            self.r.set(name, value, ex=ex)
        else:
            self.r.set(name, value)

    def get(self, name):
        return self.r.get(name)

    def s_exist(self, name, member):
        return self.r.sismember(name, member)


