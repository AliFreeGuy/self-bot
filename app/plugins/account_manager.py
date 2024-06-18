from utils import cache , btn , text  , all_admins , deleter , alert , logger  , check_phone_number , random_code  ,save_account
from utils import filters as f
from pyrogram import Client 
from config import ADMIN , API_ID , API_HASH , DEBUG , PROXY , BOT_USERNAME
import asyncio
from pyrogram import errors
import os
from pyromod import listen
from utils import run_docker
import config
from utils.utils import get_user_gap , set_user_gap
from pyrogram.enums import ChatType
from utils import utils



PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))


@Client.on_callback_query(f.is_admin , group=1)
async def account_manager_handler(client , call ):
    data = call.data.split(':')
    status = data[1]

    
    if data[0] == 'manager':


        if status == 'accounts' :
            await accounts_list(client , call )
        
        elif status == 'add_account' :
            await add_account(client , call )
        
        elif status == 'manage' : 
            await account_manager(client , call )
        
        elif status == 'back_to_accounts' :
            await accounts_list(client , call )

        elif status == 'remove_account' :
            await remove_account(client ,call )

        elif status == 'status_account' : 
            await change_status_account(client , call )
        
        elif status == 'create_session' :
            await create_session(client , call )

#         elif status == 'auto_answer' :
#             await auto_answer(client , call )

#         elif status == 'msg_timer' :
#             await msg_timer(client , call)
            
        



# async def auto_answer(bot , call ):
#     user_phone = call.data.split(':')[2]
#     answer = None
#     question = None 
#     day_limit = None 



#     try :
        
#         answer = await bot.ask(call.from_user.id  , text.a_text , timeout = 60)
#     except :await deleter(bot , call , call.message.id +1   )


#     try :
        
#         question = await bot.ask(call.from_user.id  , text.q_text, timeout = 60)
#     except :await deleter(bot , call , call.message.id +1   )


#     try :
        
#         day_limit = await bot.ask(call.from_user.id  , text.day_limit ,timeout = 60)
#     except :await deleter(bot , call , call.message.id +1   )
    


#     if answer and answer.text :
#         if question :
#             if day_limit and day_limit.text  :
#                 if day_limit.text.isdigit():


#                     answer_key  = f'autoAnswer:{user_phone}:{str(random_code())}'
#                     answer_data = {
#                                         'phone' : user_phone  ,
#                                         'answer' : answer.text ,
#                                         'question' : str(question.message.id) ,
#                                         'chat_id' : str(call.from_user.id) , 
#                                         'limit' : str(day_limit.text)
#                                         }
#                     cache.redis.hmset(answer_key , answer_data)

            
#             else :await deleter(bot , call , call.message.id +1   )
#         else :await deleter(bot , call , call.message.id +1   )
#     else :await deleter(bot , call , call.message.id +1   )

    
    
    









# async def msg_timer(bot , msg ):
#     print('fuck you user ')






































async def create_session(client , call ):
    phone_number = call.data.split(':')[2]
    account_key = f'account:{phone_number}'
    account_data = cache.get_account(account_key)

    if phone_number  and check_phone_number(phone_number) :
        phone_number = phone_number
        session_name = str(random_code())
        BASE_DIR  = os.getcwd()
        session_path = f'accounts_session/{session_name}'
        if config.DEBUG == True or config.DEBUG == 'True' :
            account = Client(session_path, API_ID, API_HASH   , proxy= config.PROXY )
        else :
            account = Client(session_path, API_ID, API_HASH   )

        await account.connect()
        
        sent_code = await account.send_code(phone_number)
        code = await client.ask(chat_id=call.from_user.id, text=text.send_code)

        if not code.text.lower().startswith('a'):
           
            await deleter(client , call , message_id=call.message.id +1)
            await alert(client , call , message=text.err_code_format)

        elif code.text.lower().startswith('a'):
            user_code = code.text.replace('a' , '')

            try :
                signed_in = await account.sign_in(phone_number, sent_code.phone_code_hash, user_code)
                try :
                    session_string = await account.export_session_string()
                    cache.redis.hset(name=account_key , key='session_string' , value=session_string)
                    logger.warning(session_string)
                    await alert(client , call , message='سشن با موفقیت دریافت شد !')
                except Exception as e :logger.warning(e)
                await account.disconnect()
                await deleter(client , call , message_id=call.message.id +1)

            except errors.SessionPasswordNeeded as e:
                logger.warning(e)
                password_hint = await account.get_password_hint()
                password = await client.ask(chat_id=call.from_user.id, text=text.enter_password(password_hint))
                try :
                    await account.check_password(password.text)
                    try :
                        session_string = await account.export_session_string()
                        cache.redis.hset(name=account_key , key='session_string' , value=session_string)
                        logger.warning(session_string)
                        await alert(client , call , message='سشن با موفقیت دریافت شد !')
                    except Exception as e : logger.warning(e)
                    await account.disconnect()
                    await deleter(client , call , message_id=call.message.id +1)



                except errors.PasswordHashInvalid as e :
                    logger.warning(e)
                    await deleter(client , call , message_id=call.message.id +1)
                    await alert(client , call , message=text.password_is_wrong)

    
        
            except errors.PhoneCodeInvalid as e:
                logger.warning(e)
                await deleter(client , call , message_id=call.message.id +1)
                await alert(client , call , message=text.code_is_wrong)

            except errors.PhoneCodeExpired as e :
                logger.warning(e)
                await deleter(client , call , message_id=call.message.id +1)
                await alert(client , call , message=text.code_is_broken)

                
            except Exception as e :
                logger.warning(e)
                await deleter(client  , call , message_id=call.message.id +1)

    else :
        await deleter(client , call , message_id=call.message.id +1)
        await alert(client , call , message=text.error_alert)

    




async def change_status_account(client , call ):
    account_data = cache.redis.hgetall(f'account:{call.data.split(":")[2]}')
    if account_data : 
        account_status = 'on' if account_data['status'] == 'off' else 'off'
        cache.redis.hset(f'account:{call.data.split(":")[2]}' , 'status'  , account_status)
        await account_manager(client , call )



async def remove_account(client , call ):
    account_data = cache.redis.hgetall(f'account:{call.data.split(":")[2]}')
    if account_data : 
        cache.redis.hset(f'account:{call.data.split(":")[2]}' , 'is_delete'  , 'True')
        await accounts_list(client , call )



async def account_manager(clietn ,call ):
    account_data = cache.redis.hgetall(f'account:{call.data.split(":")[2]}')
    account_gaps = get_user_gap(call.data.split(":")[2])

    if account_data : 
        try :
            await clietn.edit_message_text(chat_id = call.from_user.id ,
                                                text = text.account_manager(account_data['phone']) ,
                                                reply_markup = btn.account_manager(account_data ),
                                                message_id = call.message.id)
        except Exception as e  :
            print(e)
            pass
    
        





async def accounts_list(client , call ):
    all_accounts  = cache.redis.keys(f'account:*')
    accounts = []
    for i in all_accounts :
        data = cache.redis.hgetall(i)
        if data['is_delete'] == 'False':
            accounts.append(i.split(':')[1])
    try :
        await client.edit_message_text(chat_id = call.from_user.id ,
                                            text = text.accounts_list_text ,
                                            reply_markup = btn.accounts_list(accounts),
                                            message_id = call.message.id)
    except :pass





async def add_account(client ,call ):
    phone_number = None 
    try :
        await deleter(client , call , call.message.id +1   )
        phone_number  = await client.ask( chat_id = call.from_user.id ,text =text.send_phone , timeout = 60 )
    except :
        await deleter(client , call , call.message.id +1   )

        

    
    if phone_number and phone_number.text and check_phone_number(phone_number.text) :
        phone_number = phone_number.text
        session_name = str(random_code())
        BASE_DIR  = os.getcwd()
        session_path = f'accounts_session/{session_name}'
        if config.DEBUG == True or config.DEBUG == 'True' :
            account = Client(session_path, API_ID, API_HASH   , proxy= config.PROXY )
        else :
            account = Client(session_path, API_ID, API_HASH   )

        await account.connect()
        
        sent_code = await account.send_code(phone_number)
        code = await client.ask(chat_id=call.from_user.id, text=text.send_code)

        if not code.text.lower().startswith('a'):
           
            await deleter(client , call , message_id=call.message.id +1)
            await alert(client , call , message=text.err_code_format)

        elif code.text.lower().startswith('a'):
            user_code = code.text.replace('a' , '')

            try :
                signed_in = await account.sign_in(phone_number, sent_code.phone_code_hash, user_code)
                try :
                    message_data = await account.send_message(BOT_USERNAME , f'/start-{str(random_code())}')
                    session_string = await account.export_session_string()
                    logger.warning(session_string)
                    save_account(path=session_path , phone_number=phone_number , session_name=session_string , status='on' ,chat_id =  message_data.from_user.id)

            
                except Exception as e :logger.warning(e)


                await account.disconnect()
                await deleter(client , call , message_id=call.message.id +1)
                run_docker(phone_number)    
                await accounts_list(client , call )

            except errors.SessionPasswordNeeded as e:
                logger.warning(e)
                password_hint = await account.get_password_hint()
                password = await client.ask(chat_id=call.from_user.id, text=text.enter_password(password_hint))
                try :
                    await account.check_password(password.text)
                    try :
                        # print(BOT_USERNAME)
                        message_data = await account.send_message(BOT_USERNAME , f'/start-{str(random_code())}')
                        session_string = await account.export_session_string()
                        logger.warning(session_string)
                        save_account(path=session_path , phone_number=phone_number , session_name=session_string , status='on' , chat_id = message_data.from_user.id)


                    except Exception as e : logger.warning(e)



            
                    await account.disconnect()
                    await deleter(client , call , message_id=call.message.id +1)
                    run_docker(phone_number)
                    await accounts_list(client , call )



                except errors.PasswordHashInvalid as e :
                    logger.warning(e)
                    await deleter(client , call , message_id=call.message.id +1)
                    await alert(client , call , message=text.password_is_wrong)

    
        
            except errors.PhoneCodeInvalid as e:
                logger.warning(e)
                await deleter(client , call , message_id=call.message.id +1)
                await alert(client , call , message=text.code_is_wrong)

            except errors.PhoneCodeExpired as e :
                logger.warning(e)
                await deleter(client , call , message_id=call.message.id +1)
                await alert(client , call , message=text.code_is_broken)

                
            except Exception as e :
                logger.warning(e)
                await deleter(client  , call , message_id=call.message.id +1)

    else :
        await deleter(client , call , message_id=call.message.id +1)
        await alert(client , call , message=text.error_alert)
