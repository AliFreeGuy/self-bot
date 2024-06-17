import redis
import config



class CacheService:
    def __init__(self):
        self.redis = redis.StrictRedis(
            connection_pool=redis.ConnectionPool(
                host = config.REDIS_HOST, port=config.REDIS_PORT, db=config.REDIS_DB, decode_responses=True))



    def set_data(self, key, value):
        self.redis.set(key, value)

    def get_data(self, key):
        return self.redis.get(key)

    def delete_data(self, key):
        self.redis.delete(key)

    def get_account(self , key):
        return self.redis.hgetall(key)



cache = CacheService()



   
