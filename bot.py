from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackContext

# إعداد المعلومات الأساسية
TOKEN = "7960611747:AAF__2eag5N3R-5tLiy6Myq3rrNUOqzelWk"
CHANNEL_LINK = "https://t.me/awstech"
REFERRAL_LINK = "https://t.me/DurovCapsBot?start=YOUR_REFERRAL_CODE"
ADMIN_ID = "6169753913"

# وظيفة بدء البوت
async def start(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    user_name = update.effective_user.username or update.effective_user.first_name or "User"

    # رسالة الأزرار
    keyboard = [
        [InlineKeyboardButton("Let’s Go", url=REFERRAL_LINK)],
        [InlineKeyboardButton("Join the Channel", url=CHANNEL_LINK)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        f"🎉 **مرحبًا بك، {user_name}!** ⭐️\n"
        "هل هو مجرد Caps أم شيء أكبر؟\n\n"
        "اربح التذاكر بطريقتك - قم بإتمام المهام أو دعوة أصدقائك!\n\n"
        "🎉 **Welcome aboard, {user_name}!** ⭐️\n"
        "Is it just Caps, or something more?\n\n"
        "Earn tickets your way - tackle tasks or bring friends along!",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

    # إرسال إشعار للأدمن عند دخول مستخدم جديد
    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"👤 مستخدم جديد دخل البوت: @{user_name} (ID: {user_id})"
    )

# الإعداد الرئيسي للبوت
def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.run_polling()

if __name__ == "__main__":
    main()
