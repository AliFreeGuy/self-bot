from pyrogram import Client   , filters
import redis
import datetime
import jdatetime
import time
import random
from os import environ as env



API_ID=env.get('API_ID')
API_HASH=env.get('API_HASH')
PHONE_NUMBER = env.get('PHONE_NUMBER')
SESSION = env.get('SESSION')
phone_number =PHONE_NUMBER

r = redis.Redis(host='172.17.0.2' , port=6379 , db=0 , decode_responses=True)
bot = Client(str(PHONE_NUMBER) , api_id = API_ID, api_hash = API_HASH  , session_string = SESSION)


async def answer_filter(_ , cli , msg ):
    answers = [r.hgetall(answer) for answer in r.keys(f'answer:{phone_number}:*')]
    a = [a['answer'] for a in answers]
    if msg.text and msg.text in a :return True
    return False



@bot.on_message(filters.private & filters.create(answer_filter))
async def auto_answer_manager(bot , msg ):
    answers = [r.hgetall(answer) for answer in r.keys(f'answer:{phone_number}:*')]
    for answer in answers :

        if answer['answer'] == msg.text :
                limit_key = f'a_limit:{msg.chat.id}:{answer["id"]}'

                if answer.get('limit'):
                    if not r.exists(limit_key):
                        message = await bot.get_messages(int(answer['q_chat_id']), int(answer['q_message_id']))
                        if message :
                            r.setex(limit_key , int(answer['limit']) , '1')
                            await message.copy(msg.chat.id)
                            await bot.read_chat_history(msg.chat.id)
                    else :
                        user_msg_limit = r.get(limit_key)
                        if user_msg_limit == '1' :
                            r.setex(limit_key , r.ttl(limit_key) , '2')
                            await bot.send_message(chat_id = msg.chat.id , text = f'لطفا بعد از {str(r.ttl(limit_key))} ثانیه دیگه امتحان کنید .')
                            await bot.read_chat_history(msg.chat.id)
                        elif user_msg_limit == '2' :
                            r.setex(limit_key , r.ttl(limit_key) , '5')
                else :
                    message = await bot.get_messages(int(answer['q_chat_id']), int(answer['q_message_id']))
                    if message :
                        await bot.read_chat_history(msg.chat.id)
                        await message.copy(msg.chat.id)
                

        



@bot.on_message(filters.private)
async def manager(bot , msg ):

    account = r.hgetall(f'account:{phone_number}')

    if account and account['is_delete']== 'False' and account['status'] == 'on':

        
        if msg.from_user and msg.from_user.is_self :
            if msg.reply_to_message :
                await reply_manager(bot , msg)
                
            elif not msg.reply_to_message and msg.text  : 
                    await message_manager(bot , msg )

        else :
            await user_manager(bot , msg )
            





























# -------------------------------------------------------------- user manager ------------------------------------------------------------------------------


async def user_manager(bot , msg):
     
     if msg.text :
          
          
          if msg.text == 'وضعیت' :
                user_key = f'user:{phone_number}:{str(msg.chat.id)}'
                if r.exists(user_key):
                    user_data = r.hgetall(user_key)
                    start_date_timestamp = float(user_data['start_date'])
                    end_date_timestamp = float(user_data['end_date'])

                    start_date_gregorian = datetime.datetime.fromtimestamp(start_date_timestamp)
                    end_date_gregorian = datetime.datetime.fromtimestamp(end_date_timestamp)
                    current_datetime = datetime.datetime.now()
                    time_left_delta = end_date_gregorian - current_datetime
                    days_left = time_left_delta.days
                    start_date_shamsi = jdatetime.datetime.fromgregorian(datetime=start_date_gregorian)
                    end_date_shamsi = jdatetime.datetime.fromgregorian(datetime=end_date_gregorian)
                    text  = f'''
تاریخ شروع اشتراک : `{start_date_shamsi.strftime('%Y/%m/%d')}`
تاریخ پایان اشتراک : `{end_date_shamsi.strftime('%Y/%m/%d')}`
`{days_left}` روز مانده به پایان اشتراک '''
                    await bot.send_message(msg.from_user.id , text)
                else:await bot.send_message(msg.from_user.id , '❎ حساب شما اشتراکی ندارد')
            






# -------------------------------------------------------------- reply manager ------------------------------------------------------------------------------

async def reply_manager(bot , msg ) :
        target_message_id = msg.reply_to_message.id
        target_chat_id = msg.reply_to_message.chat.id
        message = await bot.get_messages(target_chat_id, target_message_id)
        status = msg.text.split(':')[0]

        
        if status == 'پیام همگانی':
            users = [r.hgetall(user) for user in r.keys(f'user:{phone_number}:*')]
            for user in users :
                await message.copy(int(user['chat_id']))
            await msg.edit_text('پیام با موفقیت به همه کاربر ها ارسال شد 🫡')
        

        elif status == 'فوروارد همگانی'  :
            users = [r.hgetall(user) for user in r.keys(f'user:{phone_number}:*')]
            for user in users :
                await message.forward(int(user['chat_id']))
            await msg.edit_text('پیام با موفقیت به همه کاربر ها فوروارد شد 🫡')

        
        elif status == 'خودکار' : 
            await auto_message_manager(bot ,msg )
            
        elif status == 'تایمر' :
            await timer_message(bot , msg )









async def timer_message(bot, msg):
    data = msg.text.split(':')
    target_message_id = msg.reply_to_message.id
    target_chat_id = msg.reply_to_message.chat.id
    
    if len(data) == 2:
        try:
            timer = int(data[1])
            timer_id = str(random.randint(1111, 99999))
            timer_key = f'timer:{phone_number}:{timer_id}'
            timer_data = {
                'phone': phone_number,
                'timer': timer,
                't_message_id': target_message_id,
                't_chat_id': target_chat_id,
                'id': timer_id
            }
            
            r.hmset(timer_key, timer_data)
            await msg.edit_text('تایمر خودکار با موفقیت ثبت شد 🫡')
            
        except Exception as e : print(e)




async def auto_message_manager(bot , msg ):
    data = msg.text.split(':')
    target_message_id = msg.reply_to_message.id
    target_chat_id = msg.reply_to_message.chat.id
    answer , limit  = None , None 

    if len(data) in (2, 3):
        answer = data[1]
        limit = data[2] if len(data) == 3 and data[2].isdigit() else None

    if answer :
        answer_id = str(random.randint(1111 , 99999))
        answer_key = f'answer:{phone_number}:{answer_id}'
        answer_data = {
                        'phone' : phone_number ,
                        'answer' : answer ,
                        'q_message_id' : target_message_id ,
                        'q_chat_id' : target_chat_id ,
                        'id' : answer_id
                   }
        
        if limit : answer_data['limit']  = int(limit)
        r.hmset(answer_key , answer_data)
        await msg.edit_text('پاسخ خودکار با موفقیت ثبت شد 🫡')




        
         
    






















































# -------------------------------------------------------------- message manager ------------------------------------------------------------------------------

async def message_manager(bot , msg ):
    status = msg.text.split(':')[0]


    if status == 'امار' : 
                users = [r.hgetall(user) for user in r.keys(f'user:{phone_number}:*')]
                await msg.edit_text(f'آمار کاربران ثبت شده : {str(len(users))}')



    if status == 'ثبت کاربر' : 
        user_key =f'user:{phone_number}:{str(msg.chat.id)}'
        user_data = {
                        'chat_id' : msg.chat.id ,
                        'name' : msg.chat.first_name ,
                        'sub' : phone_number ,
                        'end_date' : str(datetime.datetime.timestamp(msg.date + datetime.timedelta(days=30))),
                        'start_date' : str(datetime.datetime.timestamp(msg.date))

                        }
        r.hmset(user_key , user_data)
        await msg.edit_text(f'✅ کاربر با موفقیت ثبت شد')
    



    
    elif status == 'حذف کاربر' : 
        user_key =f'user:{phone_number}:{str(msg.chat.id)}'
        if r.exists(user_key):
             r.delete(user_key)
             await msg.edit_text(f'✅ کاربر با موفقیت حذف شد')
        else :
            await msg.edit_text(f'❎ این کاربر در لیست نیست')


    elif  status == 'وضعیت':
        user_key = f'user:{phone_number}:{str(msg.chat.id)}'
        if r.exists(user_key):
            user_data = r.hgetall(user_key)
            start_date_timestamp = float(user_data['start_date'])
            end_date_timestamp = float(user_data['end_date'])

            start_date_gregorian = datetime.datetime.fromtimestamp(start_date_timestamp)
            end_date_gregorian = datetime.datetime.fromtimestamp(end_date_timestamp)
            current_datetime = datetime.datetime.now()
            time_left_delta = end_date_gregorian - current_datetime
            days_left = time_left_delta.days
            start_date_shamsi = jdatetime.datetime.fromgregorian(datetime=start_date_gregorian)
            end_date_shamsi = jdatetime.datetime.fromgregorian(datetime=end_date_gregorian)
            text  = f'''
تاریخ شروع اشتراک : `{start_date_shamsi.strftime('%Y/%m/%d')}`
تاریخ پایان اشتراک : `{end_date_shamsi.strftime('%Y/%m/%d')}`
`{days_left}` روز مانده به پایان اشتراک '''
            await msg.edit_text(text)
        else:await msg.edit_text('❎ کاربر ثبت نشده')

















bot.run()
