from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes, ConversationHandler
from keyboard import Keyboard
from db_manager import DbManager 


class UserProfile:
    SHOW_PROFILE_OPTIONS, PROFILE_FIRST_NAME, PROFILE_LAST_NAME, PROFILE_PHONE, PROFILE_UNIVERSITY, PROFILE_ENTRY_YEAR = range(6)

    
    @staticmethod
    async def start_profile_registration(update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.effective_user
        telegram_id = user.id
        existing_profile = DbManager.get_user_profile(user.id)
        if DbManager.is_active(telegram_id):
            if existing_profile:

                context.user_data['existing_profile'] = existing_profile
                
                keyboard = [
                    [KeyboardButton("✏️ ویرایش پروفایل")],
                    [KeyboardButton("بازگشت 🔙")]
                ]
                
                await update.message.reply_text(
                    f"📝 پروفایل فعلی شما:\n"
                    f"👤 نام: {existing_profile.get('first_name', 'ثبت نشده')}\n"
                    f"👥 نام خانوادگی: {existing_profile.get('last_name', 'ثبت نشده')}\n"
                    f"📞 شماره تلفن: {existing_profile.get('phone', 'ثبت نشده')}\n"
                    f"🏫 دانشگاه: {existing_profile.get('university', 'ثبت نشده')}\n"
                    f"📅 سال ورودی: {existing_profile.get('entry_year', 'ثبت نشده')}\n"
                    f"گزینه مورد نظر را انتخاب کنید:",
                    reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
                )
                return UserProfile.SHOW_PROFILE_OPTIONS 
            else:
                await update.message.reply_text(
                    "👤 لطفاً نام خود را وارد کنید:",
                    reply_markup=Keyboard.back()
                )
                return UserProfile.PROFILE_FIRST_NAME
        else:
            await context.bot.send_message(chat_id=telegram_id, text="❌ کاربری شما غیرفعال است.")
            return ConversationHandler.END
        
        
    @staticmethod
    async def handle_profile_options(update: Update, context: ContextTypes.DEFAULT_TYPE):
        text = update.message.text
        
        if text == "✏️ ویرایش پروفایل":
            await update.message.reply_text(
                f"👤 نام خود را وارد کنید:",
                reply_markup=Keyboard.back()
            )
            return UserProfile.PROFILE_FIRST_NAME
            
        elif text =="بازگشت 🔙" :
            return await UserProfile.cancel_profile_registration(update, context)    
        
        
    @staticmethod  
    async def handle_first_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
        text = update.message.text
        
        if text =="بازگشت 🔙":
            return await UserProfile.cancel_profile_registration(update, context)
        
        first_name = update.message.text.strip()
        
        if len(first_name) < 2:
            await update.message.reply_text(
                "❌ نام وارد شده کوتاه است. لطفاً نام خود را وارد کنید:",
                reply_markup=Keyboard.back()
            )
            return UserProfile.PROFILE_FIRST_NAME 
        
        context.user_data['profile_first_name'] = first_name
        await update.message.reply_text(
            "👥 نام‌خانوادگی خود را وارد کنید:",
            reply_markup=Keyboard.back()
        )
        return UserProfile.PROFILE_LAST_NAME  

    @staticmethod  
    async def handle_last_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
        text = update.message.text
        last_name = update.message.text.strip()
        if text =="بازگشت 🔙":
            return await UserProfile.cancel_profile_registration(update, context)
        
        if len(last_name) < 2:
            await update.message.reply_text(
                "❌ نام خانوادگی وارد شده کوتاه است. لطفاً نام خانوادگی خود را وارد کنید:",
                reply_markup=Keyboard.back()
            )
            return UserProfile.PROFILE_LAST_NAME  
        
        context.user_data['profile_last_name'] = last_name
        await update.message.reply_text(
            "📞 حالا شماره تلفن خود را وارد کنید:",
            reply_markup=Keyboard.back()
        )
        return UserProfile.PROFILE_PHONE  

    @staticmethod 
    async def handle_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
        text = update.message.text
        
        if text =="بازگشت 🔙":
            return await UserProfile.cancel_profile_registration(update, context)
        
        phone = update.message.text.strip()
        
        if not phone.isdigit() or len(phone) < 11:
            await update.message.reply_text(
                "❌ شماره تلفن معتبر نیست. لطفاً شماره صحیح را وارد کنید :",
                reply_markup=Keyboard.back()
            )
            return UserProfile.PROFILE_PHONE 
        
        context.user_data['profile_phone'] = phone
        await update.message.reply_text(
            "🏫 نام دانشگاه خود را وارد کنید:",
            reply_markup=Keyboard.back()
        )
        return UserProfile.PROFILE_UNIVERSITY  

    @staticmethod 
    async def handle_university(update: Update, context: ContextTypes.DEFAULT_TYPE):
        text = update.message.text
        
        if text =="بازگشت 🔙":
            return await UserProfile.cancel_profile_registration(update, context)
        university = update.message.text.strip()
        
        if len(university) < 2:
            await update.message.reply_text(
                "❌ نام دانشگاه کوتاه است. لطفاً نام کامل دانشگاه را وارد کنید:",
               reply_markup=Keyboard.back()
            )
            return UserProfile.PROFILE_UNIVERSITY 
        
        context.user_data['profile_university'] = university
        await update.message.reply_text(
            "📅 سال ورودی خود را وارد کنید (مثال: 1402):",
            reply_markup=Keyboard.back()
        )
        return UserProfile.PROFILE_ENTRY_YEAR  

    @staticmethod  
    async def handle_entry_year(update: Update, context: ContextTypes.DEFAULT_TYPE):
        text = update.message.text
        
        if text =="بازگشت 🔙":
            return await UserProfile.cancel_profile_registration(update, context)
        
        entry_year = update.message.text.strip()

        try:
            year = int(entry_year)
            if year < 1350 or year > 1450:
                raise ValueError
        except ValueError:
            await update.message.reply_text(
                "❌ سال ورودی معتبر نیست. لطفاً سال صحیح را وارد کنید (مثال: 1402):",
                reply_markup=Keyboard.back()
            )
            return UserProfile.PROFILE_ENTRY_YEAR
        
        user = update.effective_user
        profile_data = {
            'first_name': context.user_data['profile_first_name'],
            'last_name': context.user_data['profile_last_name'],
            'phone': context.user_data['profile_phone'],
            'university': context.user_data['profile_university'],
            'entry_year': entry_year
        }
        
        DbManager.save_user_profile(user.id, profile_data)
        
        await update.message.reply_text(
            f"✅ پروفایل شما با موفقیت ثبت/ویرایش شد!\n\n"
            f"👤 نام: {profile_data['first_name']}\n"
            f"👥 نام خانوادگی: {profile_data['last_name']}\n"
            f"📞 تلفن: {profile_data['phone']}\n"
            f"🏫 دانشگاه: {profile_data['university']}\n"
            f"📅 سال ورودی: {profile_data['entry_year']}\n\n"
            f"بازگشت به منوی اصلی...",
            reply_markup=Keyboard.main_menu_keyboard()
        )
        
        context.user_data.clear()
        return ConversationHandler.END
    
    @staticmethod
    async def cancel_profile_registration(update: Update, context: ContextTypes.DEFAULT_TYPE):
        keys_to_remove = ['profile_first_name', 'profile_last_name', 'profile_phone', 
                         'profile_university', 'profile_entry_year', 'existing_profile']
        for key in keys_to_remove:
            context.user_data.pop(key, None)
        
        await update.message.reply_text(
            "❌ ثبت پروفایل لغو شد. به منوی اصلی برگشتید.",
            reply_markup=Keyboard.main_menu_keyboard()
        )
        return ConversationHandler.END