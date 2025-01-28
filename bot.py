from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackContext
import requests

# إعداد المعلومات الأساسية
TOKEN = "7960611747:AAF__2eag5N3R-5tLiy6Myq3rrNUOqzelWk"  # التوكن الخاص بالبوت
CHANNEL_USERNAME = "@awstech"  # معرف القناة العامة
CHANNEL_LINK = f"https://t.me/{CHANNEL_USERNAME.strip('@')}"  # رابط القناة العامة
REFERRAL_LINK = "https://t.me/DurovCapsBot?start=YOUR_REFERRAL_CODE"  # الرابط الصحيح للإحالة
ADMIN_ID = "6169753913"  # معرف الأدمن

# وظيفة التحقق من الاشتراك
def is_user_subscribed(user_id):
    url = f"https://api.telegram.org/bot{TOKEN}/getChatMember"
    params = {"chat_id": CHANNEL_USERNAME, "user_id": user_id}
    response = requests.get(url, params=params).json()

    if response.get("ok"):
        status = response["result"]["status"]
        return status in ("member", "administrator", "creator")  # المستخدم مشترك
    return False

# وظيفة بدء البوت
async def start(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    user_name = update.effective_user.username or update.effective_user.first_name or "User"

    # التحقق من اشتراك المستخدم
    if not is_user_subscribed(user_id):
        # رسالة الاشتراك الإجباري
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
