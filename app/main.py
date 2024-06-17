
from pyrogram import Client
import config 
from pyromod import listen
print(config.DEBUG)


if config.DEBUG == 'True' or config.DEBUG == True :
    
    bot = Client(
        config.BOT_SESSION,
        config.API_ID,
        config.API_HASH,
        bot_token=config.BOT_TOKEN,
        workdir=config.WORK_DIR,
        proxy=config.PROXY ,
        plugins=dict(root="plugins")
    )
else :
    bot = Client(
        config.BOT_SESSION,
        config.API_ID,
        config.API_HASH,
        bot_token=config.BOT_TOKEN,
        workdir=config.WORK_DIR,
        plugins=dict(root="plugins")
    )
if __name__ == '__main__' : 
 
    bot.run()
