from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import about
from db_manager import DbManager


TOKEN = "" 
try:
    with open('token.txt', 'r') as f:
        TOKEN = f.read()
except FileNotFoundError:
    print("token.txt doesnt exist!")



reply_keyboard = [
    ["درباره ما❔", "رویدادها📅"],
    ["ثبت پیشنهاد💡", "دوره‌ها📚"]
]
markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    telegram_id = user.id
    username = user.username
    first_name = user.first_name
    last_name = user.last_name

    DbManager.insert_user(telegram_id, username, first_name, last_name)
    await update.message.reply_text(
        "🎉 خوش آمدید به ربات ما! لطفاً یکی از گزینه‌ها را انتخاب کنید:",
        reply_markup=markup
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "درباره ما❔":
        await about.about_us(update, context)
    elif text == "رویدادها📅":
        await update.message.reply_text("در حال حاضر رویدادی ثبت نشده. منتظر خبرهای جدید باشید!")
    elif text == "ثبت پیشنهاد💡":
        await update.message.reply_text("لطفاً پیشنهاد خود را ارسال کنید تا بررسی شود.")
    elif text == "دوره‌ها📚":
        await update.message.reply_text("در حال حاضر اطلاعاتی ثبت نشده. منتظر خبرهای جدید باشید!")
    else:
        await update.message.reply_text("دستور نامشخص است. لطفاً از دکمه‌ها استفاده کنید.")


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_polling()

if __name__ == "__main__":
    main()
