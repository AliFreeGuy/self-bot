
from celery import Celery
from celery.schedules import crontab
from pyrogram import Client, filters
from os.path import abspath, dirname
import sys
import datetime
import jdatetime

parent_dir = dirname(dirname(abspath(__file__)))
sys.path.insert(0, parent_dir)
import time
import config
from utils import cache
from config import REDIS_DB, REDIS_HOST, REDIS_PORT
app = Celery('tasks', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')
app.conf.timezone = 'UTC'

app.conf.update(
    task_serializer='json',
    result_serializer='json',
    accept_content=['json',],
    worker_concurrency=1,
    worker_prefetch_multiplier=1,
)

app.conf.beat_schedule = {
    'check-stream-every-10-seconds': {
        'task': 'tasks.checker',
        'schedule': 10.0, 
    },
}
thenmin =datetime.datetime.now() + datetime.timedelta(minutes=1)
@app.task(name='tasks.checker', bind=True, default_retry_delay=1,)
def checker(self):
    try :
        accounts = cache.redis.keys(f'account:*')
        
        for acc in accounts: 
            acc_data = cache.redis.hgetall(acc)
            acc_users = [cache.redis.hgetall(user) for user in cache.redis.keys(f'user:{acc_data["phone"]}:*')]
            acc_timer_msg = [cache.redis.hgetall(timer) for timer in cache.redis.keys(f'timer:{acc_data["phone"]}:*')]
            
            for user in acc_users:
                start_date_timestamp = float(user['start_date'])
                end_date_timestamp = float(user['end_date'])
                start_date_gregorian = datetime.datetime.fromtimestamp(start_date_timestamp)
                end_date_gregorian = datetime.datetime.fromtimestamp(end_date_timestamp)
                current_datetime = datetime.datetime.now()
                time_left_delta = end_date_gregorian - current_datetime
                days_left = time_left_delta.days
                start_date_shamsi = jdatetime.datetime.fromgregorian(datetime=start_date_gregorian)
                end_date_shamsi = jdatetime.datetime.fromgregorian(datetime=end_date_gregorian)
                start = start_date_shamsi.strftime('%Y/%m/%d')
                end = end_date_shamsi.strftime('%Y/%m/%d')
                day = str(days_left)

                if days_left >= 0:
                    for timer in acc_timer_msg:
                        if int(timer['timer']) < 0:
                            timer_day = int(str(timer['timer']).replace('-', ''))
                            scheduled_time = end_date_gregorian - datetime.timedelta(days=timer_day)
                        elif int(timer['timer']) > 0:
                            timer_day = int(timer['timer'])
                            scheduled_time = start_date_gregorian + datetime.timedelta(days=timer_day)
                        
                        
                    
                        if 0 <= (scheduled_time - current_datetime ).total_seconds() <= 9:
                            print('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< starting timer message  >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
                            if config.DEBUG == 'True' or config.DEBUG == True :
                                print(acc_data['session_string'])
                                bot = Client('sender' , api_id=config.API_ID , api_hash=config.API_HASH ,session_string=acc_data['session_string'], proxy=config.PROXY)
                            else :
                                bot = Client('sender' , api_id=config.API_ID , api_hash=config.API_HASH , session_string=acc_data['session_string'] )
        
                
                            with bot :
                                msg = bot.get_messages(chat_id=int(timer['t_chat_id']) , message_ids=int(timer["t_message_id"]))
                                if msg :
                                    msg.copy(user['chat_id'])
                                
                else:print(f'<<< user sub expired >>>')
                print(100 * '-')
    except Exception as e :
        print(str(e))