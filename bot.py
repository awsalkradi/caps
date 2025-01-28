from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackContext

# إعداد المعلومات الأساسية
TOKEN = "7960611747:AAF__2eag5N3R-5tLiy6Myq3rrNUOqzelWk"  # التوكن الخاص بالبوت
CHANNEL_LINK = "https://t.me/+xUCQE-w8QCszZTAy"  # رابط الدعوة للقناة
REFERRAL_LINK = "https://t.me/DurovCapsBot?start=YOUR_REFERRAL_CODE"  # الرابط الصحيح للإحالة
ADMIN_ID = "6169753913"  # معرف الأدمن

# قائمة المستخدمين الذين أكملوا الاشتراك
subscribed_users = set()

# وظيفة بدء البوت
async def start(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    user_name = update.effective_user.username or update.effective_user.first_name or "User"

    if user_id not in subscribed_users:
        # إرسال رسالة الاشتراك الإجباري
        keyboard = [[InlineKeyboardButton("🔗 اضغط للاشتراك في القناة | Join the Channel", url=CHANNEL_LINK)]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            "📢 **لإكمال استخدام البوت، يرجى الاشتراك في القناة.**\n"
            "1️⃣ اضغط على الزر أدناه للانضمام إلى القناة.\n"
            "2️⃣ بعد الانضمام، اضغط على /start لإكمال الاستخدام.\n\n"
            "📢 **To continue using the bot, please subscribe to the channel.**\n"
            "1️⃣ Click the button below to join the channel.\n"
            "2️⃣ After joining, click /start to proceed.",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
        # تسجيل المستخدم في القائمة لتجنب تكرار رسالة الاشتراك
        subscribed_users.add(user_id)
        return  # إنهاء الوظيفة إذا لم يكن المستخدم مسجلًا بعد

    # إذا كان المستخدم قد اشترك بالفعل، إرسال رسالة الأزرار
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
