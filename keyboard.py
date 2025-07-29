from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram import InlineKeyboardButton, InlineKeyboardMarkup



class Keyboard:
    
    def main_menu_keyboard():
        reply_keyboard = [
            ["درباره ما❔", "رویدادها📅"],
            ["ثبت پیشنهاد💡", "دوره‌ها📚"],
            ["ثبت یا ویرایش پروفایل کاربری👤"]
        ]
        return ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
    
    def back():
        reply_keyboard = [["بازگشت 🔙"]]
        return ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
    
    def event_register_keyboard(ev_title, ev_id):
        keyboard = [
            [InlineKeyboardButton("ثبت‌نام در رویداد ✏", callback_data=f"{ev_title}_register_{ev_id}")]
        ]

        return InlineKeyboardMarkup(keyboard)

