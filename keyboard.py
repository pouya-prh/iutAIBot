from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes


class Keyboard:
    
    def main_menu_keyboard():
        reply_keyboard = [
            ["درباره ما❔", "رویدادها📅"],
            ["ثبت پیشنهاد💡", "دوره‌ها📚"]
        ]
        return ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
    
    def back():
        reply_keyboard = [["بازگشت 🔙"]]
        return ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
