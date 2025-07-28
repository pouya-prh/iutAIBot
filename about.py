from telegram import Update
from telegram.ext import ContextTypes

async def about_us(update, context):
    try:
        with open('about.txt', 'r', encoding='utf-8') as f:
            message = f.read().strip()
        
        if message:
            await update.message.reply_text(message)
        else:
            await update.message.reply_text("در حال حاضر اطلاعاتی ثبت نشده. منتظر خبرهای جدید باشید!")

    except FileNotFoundError:
        print("فایل 'about.txt' پیدا نشد.")
    except Exception as e:
        print(f"خطا هنگام خواندن فایل: {e}")
