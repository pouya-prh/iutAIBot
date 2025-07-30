from telegram import Update
from db_manager import DbManager
from telegram.constants import ParseMode
from events import Events
def to_text(event):
        text = f"📌 <b>{event.title}</b>\n"
        text += f"{event.description}\n"
        text += f"🗓 <b>زمان:</b> {event.start_time}\n"
        if event.location:
            text += f"📍 <b>مکان:</b> {event.location}\n"
        if event.capacity:
            if event.capacity == -1 :
                text += f"👥 <b> ظرفیت: نامحدود</b>\n"
            else:    
                text += f"👥 <b>ظرفیت:</b> {event.capacity}\n"
       
        if event.payment == 0:
            text += f"💲 <b>هزینه:</b> رایگان\n"
        else:
            text += f"💲 <b>هزینه:</b> {event.payment} تومان\n"
            
        return text

async def display_user_event(update: Update, context):
    telegram_id = update.effective_user.id
    events_list = DbManager.return_user_event(telegram_id)
    
    chat_id = update.effective_chat.id

    if not events_list or len(events_list) == 0:
        await context.bot.send_message(chat_id=chat_id, text="هیچ رویدادی وجود ندارد.")
        return
    
    for ev in events_list:
        msg = to_text(ev)
        await context.bot.send_message(
            chat_id=chat_id,
            text=msg,
            parse_mode=ParseMode.HTML,
        )


def display_user_course(update, context):
    pass