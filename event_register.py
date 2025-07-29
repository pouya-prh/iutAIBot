from telegram.ext import CallbackQueryHandler
from telegram import Update
from db_manager import DbManager

async def handle_event_register_callback(update: Update, context):
    query = update.callback_query
    telegram_id = update.effective_user.id
    await query.answer()  
    if DbManager.get_user_profile(telegram_id) is None:
        await query.message.reply_text(f"لطفا ابتدا پروفایل کاربری خود را تکمیل کنید")
        return
    
    event_id = int(query.data.split("_")[2])
    event_title = query.data.split("_")[0]
    await query.message.reply_text(f"در حال ثبت‌نام در رویداد {event_title} ...")
    result = DbManager.event_register_db(telegram_id, event_id)
    register_messages = {
        "successfully registered": "ثبت‌نام شما با موفقیت انجام شد ✅",
        "already registered": "شما لیترالی قبلاً در این رویداد ثبت‌نام کرده‌اید.",
        "event is full": "ظرفیت این رویداد تکمیل شده است.",
        "user not found": "کاربری شما شناسایی نشد.",
        "user has been deactivated": "کاربری شما غیرفعال است.",
        "event not found": "رویدادی با این مشخصات یافت نشد.",
        "payment": "صفحه پرداخت باید طراحی شود"
    }
    msg = register_messages.get(result, "خطایی رخ داد. لطفاً مجدداً تلاش کنید.")

    await query.message.reply_text(msg)
    
