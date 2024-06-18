from pyrogram.types import (ReplyKeyboardMarkup, InlineKeyboardMarkup,InlineKeyboardButton , KeyboardButton , WebAppData , WebAppInfo)
from config import ADMIN



def manager_btn(chat_id ):
    buttons = []
    buttons.append([InlineKeyboardButton(text='مدیریت اکانت ها',callback_data='manager:accounts')])
    # if chat_id == ADMIN :
    #     buttons.append([InlineKeyboardButton(text='مدیریت ادمین ها',callback_data='manager:admins')])
    return InlineKeyboardMarkup(buttons)



def admins_btn(admins  ):
    buttons = []
    for admin in admins :
        if int(admin) != ADMIN :
            buttons.append([InlineKeyboardButton(text=str(admin),callback_data=f'manager:remove_admin:{str(admin)}')])
    
    buttons.append([

        InlineKeyboardButton(text='🔙',callback_data='manager:back'),
        InlineKeyboardButton(text='➕',callback_data='manager:add_admin'),
        
        ])

    return InlineKeyboardMarkup(buttons)




def accounts_list(accounts):
    buttons = []
    for account in accounts :
            buttons.append([InlineKeyboardButton(text=str(account),callback_data=f'manager:manage:{str(account)}')])
    
    
    buttons.append([

        InlineKeyboardButton(text='🔙',callback_data='manager:back'),
        InlineKeyboardButton(text='➕',callback_data='manager:add_account'),
        
        ])

    return InlineKeyboardMarkup(buttons)

def account_manager(data ):
    buttons = []
    status_text = 'اکانت روشن است' if data['status'] == 'on' else 'اکانت خاموش است'

    buttons.append([
        InlineKeyboardButton(text=status_text,callback_data=f'manager:status_account:{data["phone"]}'),        
        ])
    

    buttons.append([
        InlineKeyboardButton(text='ایجاد سشن',callback_data=f'manager:create_session:{data["phone"]}'),        
        ])
    
    buttons.append([

        InlineKeyboardButton(text='🔙',callback_data='manager:back_to_accounts'),
        InlineKeyboardButton(text='❌',callback_data=f'manager:remove_account:{data["phone"]}'),
        
        ])
    

    
    return InlineKeyboardMarkup(buttons)