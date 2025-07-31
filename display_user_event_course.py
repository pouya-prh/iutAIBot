from telegram import Update
from db_manager import DbManager
from telegram.constants import ParseMode
from events import Events
from course import Course
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import asyncio

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
    if DbManager.is_active(telegram_id):
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
    else:
        query = update.callback_query
        await query.message.reply_text("کاربری شما غیرفعال است ❌")

async def display_user_course(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.effective_user.id
    if DbManager.is_active(telegram_id):
        courses = DbManager.get_user_courses(telegram_id)

        if not courses:
            await update.message.reply_text("🎓 شما در هیچ دوره‌ای ثبت‌نام نکردید.")
            return
        keyboard = [
            [InlineKeyboardButton(text=title, callback_data=f"course:{course_id}")] for course_id, title in courses 

        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("✅ لطفاً یکی از دوره‌ها را انتخاب کنید:", reply_markup=reply_markup)
    else:
        query = update.callback_query
        await query.message.reply_text("کاربری شما غیرفعال است ❌")

async def display_course(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    telegram_id = query.from_user.id
    if DbManager.is_active(telegram_id):
        try:
            course_id = int(query.data.split(":")[1])
        except Exception:
            await context.bot.send_message(chat_id=telegram_id, text="❌ مشکلی در دریافت شناسه دوره پیش آمد.")
            return

        all_episodes = DbManager.return_all_episode_of_course(course_id)

        if not all_episodes:
            await context.bot.send_message(chat_id=telegram_id, text="❌ اپیزودی برای این دوره یافت نشد.")
            return

        for file_id, title, instructor, episode in all_episodes:
            try:
                caption = f"🎬 {title}\n👨‍🏫 مدرس: {instructor}\n🎞 قسمت: {episode}"
                await context.bot.send_video(
                    chat_id=telegram_id,
                    video=file_id,
                    caption=caption
                )
                await asyncio.sleep(0.2)
            except Exception as e:
                await context.bot.send_message(chat_id=telegram_id, text=f"❌ خطا در ارسال اپیزود {episode}:\n{str(e)}")
    else:
        await context.bot.send_message(chat_id=telegram_id, text="❌ کاربری شما غیرفعال است.")
