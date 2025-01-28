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

    # إذا كان المستخدم جديدًا ولم يتم تسجيله كمشترك
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
        return  # إنهاء الوظيفة إذا لم يكن المستخدم مشتركًا

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

    # إرسال إشعار إلى الأدمن عند دخول مستخدم جديد لأول مرة
    if user_id not in subscribed_users:
        subscribed_users.add(user_id)
        total_users = len(subscribed_users)
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"🚨 مستخدم جديد دخل البوت لأول مرة:\n\n"
                 f"👤 User ID: {user_id}\n"
                 f"📝 Username: @{user_name}\n"
                 f"📊 Total Users: {total_users}"
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
