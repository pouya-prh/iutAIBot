from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
from db_manager import DbManager
async def return_file_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.effective_user.id
    if DbManager.is_admin(telegram_id):
        video = update.message.video
        if video:
            await update.message.reply_text(f"✅ file_id:\n`{video.file_id}`")
        else:
            await update.message.reply_text("این پیام شامل ویدیو نیست.")
    else:
        await update.message.reply_text("⛔ فقط ادمین‌ها اجازه دریافت file_id را دارند.")
        
