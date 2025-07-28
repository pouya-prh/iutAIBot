from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.ext import ConversationHandler
from keyboard import Keyboard

SUGGESTION = 1 


class Suggestion:
    async def ask_for_suggestion(update: Update, context: ContextTypes.DEFAULT_TYPE):
        reply_keyboard = [["بازگشت 🔙"]]
        markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)

        await update.message.reply_text(
            "💡 لطفاً پیشنهاد خود را ارسال کنید.\nیا با 'بازگشت 🔙' به منوی اصلی برگردید.",
            reply_markup=markup
        )

        return SUGGESTION

    async def handle_suggestion(update: Update, context: ContextTypes.DEFAULT_TYPE):
        text = update.message.text

        if text == "بازگشت 🔙":
            await update.message.reply_text(
                "به منوی اصلی برگشتید.",
                reply_markup=Keyboard.main_menu_keyboard()
            )
            return ConversationHandler.END

        suggestion = text
        user = update.effective_user
        telegram_id = user.id

        print(f"🔔 Suggestion from {telegram_id}: {suggestion}")

        await update.message.reply_text(
            "✅ پیشنهاد شما دریافت شد. ممنون از همکاری شما!",
            reply_markup=Keyboard.main_menu_keyboard()
        )
        return ConversationHandler.END
