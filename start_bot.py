from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.ext import ConversationHandler, CallbackQueryHandler
import about
from db_manager import DbManager
from keyboard import Keyboard
from suggestion import Suggestion, SUGGESTION
from show_events import show_events
import event_register
from logs import Logs
from user_profile import UserProfile
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
    
    Logs.start_clicked(telegram_id,first_name)

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
    
    Logs.start()
    suggestion_conv_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex("^ثبت پیشنهاد💡$"), Suggestion.ask_for_suggestion)],
        states={
            SUGGESTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, Suggestion.handle_suggestion)],
        },
        fallbacks=[
                   MessageHandler(filters.COMMAND, Suggestion.cancel_suggestion), 
                   ]
    )
    
    profile_conv_handler = ConversationHandler(
    entry_points=[
        MessageHandler(filters.Regex("^ثبت یا ویرایش پروفایل کاربری👤$"), UserProfile.start_profile_registration),
    ],
    states={
        UserProfile.SHOW_PROFILE_OPTIONS: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, UserProfile.handle_profile_options)
        ],
        UserProfile.PROFILE_FIRST_NAME: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, UserProfile.handle_first_name)
        ],
        UserProfile.PROFILE_LAST_NAME: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, UserProfile.handle_last_name)
        ],
        UserProfile.PROFILE_PHONE: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, UserProfile.handle_phone)
        ],
        UserProfile.PROFILE_UNIVERSITY: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, UserProfile.handle_university)
        ],
        UserProfile.PROFILE_ENTRY_YEAR: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, UserProfile.handle_entry_year)
        ],
    },
    fallbacks=[
        MessageHandler(filters.COMMAND, UserProfile.cancel_profile_registration), 
    ]
)
 
    app.add_handler(profile_conv_handler)
    app.add_handler(suggestion_conv_handler) 
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(
    event_register.handle_event_register_callback, pattern=r".+_register_\d+$"))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    

    app.run_polling()

if __name__ == "__main__":
    main()
