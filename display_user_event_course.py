from telegram import Update
from db_manager import DbManager
from telegram.constants import ParseMode
from events import Events
from course import Course
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram import InlineKeyboardButton, InlineKeyboardMarkup


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


async def display_user_course(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.effective_user.id
    courses = DbManager.get_user_courses(telegram_id)

    if not courses:
        await update.message.reply_text("🎓 شما در هیچ دوره‌ای ثبت‌نام نکردید.")
        return
    keyboard = [
        [InlineKeyboardButton(text=title, callback_data=f"course:{course_id}")] for course_id, title in courses 

    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("✅ لطفاً یکی از دوره‌ها را انتخاب کنید:", reply_markup=reply_markup)

