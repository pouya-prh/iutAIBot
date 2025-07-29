from telegram.constants import ParseMode
from db_manager import DbManager
from telegram import Update
from events import Events
from keyboard import Keyboard

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
        return text

async def show_events(update: Update, context):
    events_list = DbManager.return_events()
    
    chat_id = update.effective_chat.id

    if not events_list or len(events_list) == 0:
        await context.bot.send_message(chat_id=chat_id, text="هیچ رویدادی وجود ندارد.")
        return

    for ev in events_list:
        msg = to_text(ev)
        if ev.cover_image:
            with open(ev.cover_image, "rb") as photo_file:
                await context.bot.send_photo(
                    chat_id=chat_id,
                    photo=photo_file,        
                    caption=msg,
                    parse_mode=ParseMode.HTML,
                    reply_markup = Keyboard.event_register_keyboard(ev.title, ev.ID)
                )
        else:
            await context.bot.send_message(
                chat_id=chat_id,
                text=msg,
                parse_mode=ParseMode.HTML,
                reply_markup = Keyboard.event_register_keyboard(ev.title, ev.ID)
            )
        