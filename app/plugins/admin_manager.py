from utils import cache , btn , text  , all_admins , deleter , alert , logger
from utils import filters as f
from pyrogram import Client 
from config import ADMIN




@Client.on_callback_query(f.is_admin , group=0)
async def admin_manager_handler(client , call ):
    logger.warning(f'callback data : {call.data}  - user : {call.from_user.id }')

    data = call.data.split(':')
    status = data[1]
  
    if data[0] == 'manager' :
      

        if status == 'admins'  :
            await admin_manager(client , call )
        
        elif status == 'remove_admin' :
            await remove_admin(client , call )
        
        elif status == 'back':
            await back_to_main_menu(client , call )

        elif status  == 'remove_admin':
            await remove_admin(client ,call )

        elif status == 'add_admin' :
            await add_admin(client , call )



async def add_admin(client ,call ):
    data = None 
    try :
        await deleter(client , call , call.message.id +1   )
        data = await client.ask( chat_id = call.from_user.id ,text =text.send_admin_chat_id , timeout = 60 )
    except :
        await deleter(client , call , call.message.id +1   )

        

    
    if data and data.text and data.text.isdigit() :
        cache.redis.set(f'admin:{data.text}' , 'fuck you ')
        await admin_manager(client , call )
        await deleter(client , call , call.message.id +1   )
        await alert(client , call , message=text.add_admin)


    else :
        await deleter(client , call , call.message.id +1   )
        await alert(client , call )
        


async def remove_admin(client , call ):
    admin_chat_id = call.data.split(':')[2]
    cache.redis.delete(f'admin:{admin_chat_id}')
    await admin_manager(client, call )



async def back_to_main_menu(client , call ):
        try :
            await client.edit_message_text(chat_id = call.from_user.id ,
                                                text = text.manager_text ,
                                                reply_markup = btn.manager_btn(call.from_user.id),
                                                message_id = call.message.id)
        except Exception as e :
            print(e)
            pass


        
async def admin_manager(client, call ):
    try :
        admins = all_admins()
        await client.edit_message_text(chat_id = call.from_user.id ,
                                            text = text.admin_manager_text ,
                                            reply_markup = btn.admins_btn(admins),
                                            message_id = call.message.id)

    except Exception as e :
        print(e)
        pass



