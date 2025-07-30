from telegram.constants import ParseMode
from db_manager import DbManager
from telegram import Update
from course import Course
from keyboard import Keyboard

def to_text(corese):
        text = f"📌 <b>{corese.title}</b>\n"
        text += f"{corese.description}\n"
        text += f"👨‍🏫 <b>مدرس:</b> {corese.instructor}\n"
        if corese.payment == 0:
            text += f"💲 <b>هزینه:</b> رایگان\n"
        else:
            text += f"💲 <b>هزینه:</b> {corese.payment} تومان\n"
            
        return text

async def show_courses(update: Update, context):
    course_list = DbManager.return_courses()
    
    chat_id = update.effective_chat.id

    if not course_list or len(course_list) == 0:
        await context.bot.send_message(chat_id=chat_id, text="هیچ دوره ای وجود ندارد.")
        return

    for course in course_list:
        msg = to_text(course)
        if course.cover_image:
            with open(course.cover_image, "rb") as photo_file:
                await context.bot.send_photo(
                    chat_id=chat_id,
                    photo=photo_file,        
                    caption=msg,
                    parse_mode=ParseMode.HTML,
                    reply_markup = Keyboard.course_register_keyboard(course.title, course.ID)
                )
        else:
            await context.bot.send_message(
                chat_id=chat_id,
                text=msg,
                parse_mode=ParseMode.HTML,
                reply_markup = Keyboard.course_register_keyboard(course.title, course.ID)
            )
        