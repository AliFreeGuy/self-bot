from pyrogram import Client, filters
from utils import logger
from utils import cache , btn , text
from utils import filters as f 
from config import *
from utils.utils import set_user_gap , get_user_gap ,random_code






@Client.on_message( f.is_admin , group=0)
async def start_manager(bot, msg):
    if msg.text and msg.text == '/start' : 
        logger.info(f'command : /start   -   user : {msg.from_user.id}' )
        await bot.send_message(msg.from_user.id , text.manager_text , reply_markup = btn.manager_btn(msg.from_user.id))


        # set_user_gap(user_chat_id=msg.from_user.id  , gap_chat_id=random_code() , gap_name='test', phone = '+989935599601')
        # gaps = get_user_gap('+989935599601')
        # print(gaps)







@Client.on_message( f.not_admin , group=0)
async def user_not_admin(bot, msg):
        logger.info(f'user not admin : {msg.from_user.id}' )
        await bot.send_message(msg.from_user.id , text.user_not_admin )



