from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
from db_manager import DbManager
async def return_file_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.effective_user.id
    if DbManager.is_admin(telegram_id):
        if DbManager.is_active(telegram_id):
            video = update.message.video
            if video:
                await update.message.reply_text(f"✅ file_id:\n`{video.file_id}`")
            else:
                await update.message.reply_text("این پیام شامل ویدیو نیست.")
        else:
            await context.bot.send_message(chat_id=telegram_id, text="❌ کاربری شما غیرفعال است.")
    else:
        await update.message.reply_text("⛔ فقط ادمین‌ها اجازه دریافت file_id را دارند.")
        
