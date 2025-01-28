from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackContext

# إعداد المعلومات الأساسية
TOKEN = "7960611747:AAF__2eag5N3R-5tLiy6Myq3rrNUOqzelWk"  # التوكن الخاص بالبوت
CHANNEL_LINK = "https://t.me/+xUCQE-w8QCszZTAy"  # رابط الدعوة للقناة
REFERRAL_LINK = "https://t.me/DurovCapsBot/caps?startapp=374668608"  # رابط الإحالة

# وظيفة بدء البوت
async def start(update: Update, context: CallbackContext):
    user_name = update.effective_user.username or update.effective_user.first_name or "User"

    # إعداد الأزرار
    keyboard = [
        [InlineKeyboardButton("Join the Channel", url=CHANNEL_LINK)],
        [InlineKeyboardButton("Let’s Go", url=REFERRAL_LINK)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # إرسال الرسالة مع الأزرار
    await update.message.reply_text(
        f"Welcome aboard, {user_name}! ⭐️\n"
        "Is it just Caps, or something more?\n\n"
        "Earn tickets your way - tackle tasks or bring friends along!",
        reply_markup=reply_markup
    )

# الإعداد الرئيسي للبوت
def main():
    # إنشاء تطبيق البوت
    application = Application.builder().token(TOKEN).build()

    # إضافة وظيفة /start
    application.add_handler(CommandHandler("start", start))

    # تشغيل البوت
    application.run_polling()

if __name__ == "__main__":
    main()
