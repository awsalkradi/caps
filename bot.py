import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackContext

# إعداد المعلومات الأساسية
TOKEN = "7960611747:AAF__2eag5N3R-5tLiy6Myq3rrNUOqzelWk"
CHANNEL_LINK = "https://t.me/awstech"
REFERRAL_LINK = "https://t.me/DurovCapsBot/caps?startapp=374668608"  # رابط الإحالة الجديد
ADMIN_ID = "6169753913"

# ملف تخزين المستخدمين
USERS_FILE = "subscribed_users.json"

# تحميل المستخدمين من ملف JSON
def load_users():
    try:
        with open(USERS_FILE, "r") as file:
            return set(json.load(file))
    except FileNotFoundError:
        return set()

# حفظ المستخدمين في ملف JSON
def save_users(users):
    with open(USERS_FILE, "w") as file:
        json.dump(list(users), file)

# قائمة المستخدمين
subscribed_users = load_users()

# وظيفة بدء البوت
async def start(update: Update, context: CallbackContext):
    user_id = str(update.effective_user.id)  # استخدام str لضمان التوافق مع JSON
    user_name = update.effective_user.username or update.effective_user.first_name or "User"

    if user_id not in subscribed_users:
        # تسجيل المستخدم عند أول ضغط على /start
        subscribed_users.add(user_id)
        save_users(subscribed_users)

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
        return

    # إذا كان المستخدم قد اشترك بالفعل
    keyboard = [
        [InlineKeyboardButton("Let’s Go", url=REFERRAL_LINK)],
        [InlineKeyboardButton("Join the Channel", url=CHANNEL_LINK)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # استخدام التنسيق السليم في الرسالة
    message = (
        f"🎉 **مرحبًا بك، {user_name}!** ⭐️\n\n"
        "هل هو مجرد Caps أم شيء أكبر؟\n\n"
        "اربح التذاكر بطريقتك - قم بإتمام المهام أو دعوة أصدقائك!\n\n"
        "🎉 **Welcome aboard, {user_name}!** ⭐️\n\n"
        "Is it just Caps, or something more?\n\n"
        "Earn tickets your way - tackle tasks or bring friends along!"
    )

    await update.message.reply_text(
        message,
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

    # إرسال إشعار للأدمن
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
