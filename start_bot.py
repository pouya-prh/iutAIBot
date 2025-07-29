from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.ext import ConversationHandler
import about
from db_manager import DbManager
from keyboard import Keyboard
from suggestion import Suggestion, SUGGESTION
from show_events import show_events
TOKEN = "" 
try:
    with open('token.txt', 'r') as f:
        TOKEN = f.read()
except FileNotFoundError:
    print("token.txt doesnt exist!")





async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    telegram_id = user.id
    username = user.username
    first_name = user.first_name
    last_name = user.last_name

    DbManager.insert_user(telegram_id, username, first_name, last_name)
    await update.message.reply_text(
        "🎉 خوش آمدید به ربات ما! لطفاً یکی از گزینه‌ها را انتخاب کنید:",
         reply_markup=Keyboard.main_menu_keyboard()
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "درباره ما❔":
        await about.about_us(update, context)
    elif text == "رویدادها📅":
        await show_events(update,context)
    elif text == "دوره‌ها📚":
        await update.message.reply_text("در حال حاضر اطلاعاتی ثبت نشده. منتظر خبرهای جدید باشید!")
    else:
        await update.message.reply_text("دستور نامشخص است. لطفاً از دکمه‌ها استفاده کنید.")

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    
    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex("^ثبت پیشنهاد💡$"), Suggestion.ask_for_suggestion)],
        states={
            SUGGESTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, Suggestion.handle_suggestion)],
        },
        fallbacks=[MessageHandler(filters.Regex("^بازگشت 🔙$"), Suggestion.handle_suggestion)]
    )
    app.add_handler(conv_handler)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
