from telegram import Update
from db_manager import DbManager

async def handle_course_register_callback(update: Update, context):
    telegram_id = update.effective_user.id

    if DbManager.is_active(telegram_id):
        query = update.callback_query
        await query.answer()  
        if DbManager.get_user_profile(telegram_id) is None:
            await query.message.reply_text(f"لطفا ابتدا پروفایل کاربری خود را تکمیل کنید")
            return
        
        course_id = int(query.data.split("_")[2])
        course_title = query.data.split("_")[0]
        await query.message.reply_text(f"در حال ثبت‌نام در دوره {course_title} ...")
        result = DbManager.course_register_db(telegram_id, course_id)
        register_messages = {
            "successfully registered": "ثبت‌نام شما با موفقیت انجام شد ✅",
            "already registered": "شما لیترالی قبلاً در این دوره ثبت‌نام کرده‌اید.",
            "user not found": "کاربری شما شناسایی نشد.",
            "user has been deactivated": "کاربری شما غیرفعال است.",
            "event not found": "دوره ای با این مشخصات یافت نشد.",
            "payment": "صفحه پرداخت باید طراحی شود"
        }
        msg = register_messages.get(result, "خطایی رخ داد. لطفاً مجدداً تلاش کنید.")

        await query.message.reply_text(msg)
    else:
        await context.bot.send_message(chat_id=telegram_id, text="❌ کاربری شما غیرفعال است.")
