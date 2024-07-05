from . import cache  , logger
from config import ADMIN , API_ID , API_HASH , BOT_USERNAME , FORWARDER_IMAGE_NAME 
from . import text 
import random
import docker
import config







def save_account(path , phone_number ,session_name , chat_id  ,  status = 'on' , is_delete = 'False'):
    cache.redis.hmset(f'account:{str(phone_number)}' ,
                                    {'path' : path ,
                                    'status' : status ,
                                    'phone' : phone_number ,
                                    'session_name' : session_name,
                                    'is_delete' : is_delete,
                                    'chat_id' : chat_id
                                    })
    return True




def all_admins():
    admins = [int(ADMIN)]
    all_admins = cache.redis.keys('admin:*')
    for admin in all_admins :
        admins.append(int(admin.split(':')[1]))
    return admins

def random_code() :
    return random.randint(10000 , 99999)




def check_phone_number(phone_number):
    if phone_number.startswith("+") and phone_number[1:].isdigit() and len(phone_number) > 7:
        return True
    else:
        return False
    



async def deleter(client , call , message_id ):
    try :
        message_id = message_id
        msg_ids = []
        for x in range(100) :
            msg_ids.append(message_id + x)

        print(message_id)
        print(msg_ids)
        await client.delete_messages(call.from_user.id  ,msg_ids )
    except :pass

async def alert(clietn, call , message= None  ):
    try :
        if message :
            await clietn.answer_callback_query(call.id, text=message, show_alert=True)
        else :
            await clietn.answer_callback_query(call.id, text=text.error_alert, show_alert=True)

    except :pass




def run_docker(phone ):
    logger.warning(f'running container for phone : {str(phone)}')
    print(f'running container for phone : {str(phone)}')
    try:
        account = cache.redis.hgetall(f'account:{str(phone)}')
        if account:
            container_name = f"self-{str(account['phone']).replace('+', '')}"
            image_name = FORWARDER_IMAGE_NAME
            session_string = account.get('session_name')
            if session_string:
                client = docker.from_env()
                
                # Check if a container with the same name exists
                try:
                    existing_container = client.containers.get(container_name)
                    # Stop and remove the existing container
                    existing_container.stop()
                    existing_container.remove()
                    logger.warning(f'Existing container {container_name} stopped and removed')
                except docker.errors.NotFound:
                    logger.warning(f'No existing container named {container_name} found')

                container = client.containers.run(
                    image_name,
                    name=container_name,
                    environment={
                        "API_HASH": API_HASH,
                        "API_ID": API_ID,
                        "SESSION": session_string,
                        'PHONE_NUMBER': phone,
                        'REDIS_DB': config.REDIS_DB, 
                        'REDIS_HOST': config.REDIS_HOST,
                    },
                    detach=True
                )
                logger.warning(f'Container {container_name} started with ID: {container.id}')
            else:
                logger.warning('<<< user not active session string >>>')
    except Exception as e:
        logger.warning(e)



def set_user_gap(user_chat_id , gap_chat_id , gap_name  ,phone ,  status = 'off'):

        data = {'user_chat_id' : user_chat_id , 'gap_chat_id'  : gap_chat_id , 'gap_name' : gap_name , 'status' :status , 'phone' : phone}
        key = f'userGap:{str(phone)}:{str(gap_chat_id)}'
        cache.redis.hmset(key , data)



def get_user_gap(phone ):
        key  = f'userGap:{str(phone)}:*'
        user_gaps = [cache.redis.hgetall(gaps) for gaps in cache.redis.keys(key)]
        return user_gaps

