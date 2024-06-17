import redis

redis_host = '172.17.0.3'
redis_port = 6379  # پورت جدید
r = redis.Redis(host=redis_host, port=redis_port)
r.set('admin:5522477996' , 'f')