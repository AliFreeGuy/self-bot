from pyrogram.types import (ReplyKeyboardMarkup, InlineKeyboardMarkup,InlineKeyboardButton , KeyboardButton , WebAppData , WebAppInfo)
from config import ADMIN
import datetime
import jdatetime

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
        InlineKeyboardButton(text='مدیریت کاربران',callback_data=f'manager:user_manager:{data["phone"]}'),        
        InlineKeyboardButton(text='مدیریت پیامها',callback_data=f'manager:msg_manager:{data["phone"]}'),        
        ])
    

    buttons.append([

        InlineKeyboardButton(text='🔙',callback_data='manager:back_to_accounts'),
        InlineKeyboardButton(text='❌',callback_data=f'manager:remove_account:{data["phone"]}'),
        
        ])
    

    
    return InlineKeyboardMarkup(buttons)


def user_manager_btn(users , phone ):
     
    buttons = []
    buttons.append([
        InlineKeyboardButton(text='🔙',callback_data=f'manager:back_account:{phone}'),        
        ])
    for user in users :
        try :
            start_date_timestamp = float(user['start_date'])
            end_date_timestamp = float(user['end_date'])
            start_date_gregorian = datetime.datetime.fromtimestamp(start_date_timestamp)
            end_date_gregorian = datetime.datetime.fromtimestamp(end_date_timestamp)
            current_datetime = datetime.datetime.now()
            time_left_delta = end_date_gregorian - current_datetime
            days_left = time_left_delta.days
            start_date_shamsi = jdatetime.datetime.fromgregorian(datetime=start_date_gregorian)
            end_date_shamsi = jdatetime.datetime.fromgregorian(datetime=end_date_gregorian)
            start = start_date_shamsi.strftime('%m/%d')
            end = end_date_shamsi.strftime('%m/%d')
            day = str(days_left)
            buttons.append([
            InlineKeyboardButton(text=f"{user['name']} - {start} - {end} - {day}",url=f'tg://openmessage?user_id={user["chat_id"]}'),        
            ])
        except Exception as e :
            print(e)
            continue

    

    
    return InlineKeyboardMarkup(buttons)




def answer_manager(answers , phone , timers ):
    buttons = []
    buttons.append([
    InlineKeyboardButton(text='🔙',callback_data=f'manager:back_account:{phone}'),        
    ])

    for answer in answers :
        limit_text = f'⏱ {str(answer["limit"]) if answer.get("limit") else ""} -'
        text = f'{limit_text if answer.get("limit") else ""} {answer["answer"]}'
        buttons.append([
            InlineKeyboardButton(text=text,callback_data=f'manager:rma_{str(answer["id"])}:{phone}'),        
            ])
        
    
    for timer in timers :
        
        
        if int(timer['timer']) <= 0 :
            timer_status_text = f'⏰ تایمر {str(timer["timer"].replace("-" , ""))} روز مانده به پایان'
        else : timer_status_text = f'⏰ تایمر {str(timer["timer"])} روز بعد از شروع'

        

        # text = f'{limit_text if answer.get("limit") else ""} {answer["answer"]}'
        buttons.append([
            InlineKeyboardButton(text=timer_status_text,callback_data=f'manager:rmt_{str(timer["id"])}:{phone}'),        
            ])
        

    
    return InlineKeyboardMarkup(buttons)
