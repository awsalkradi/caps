from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackContext
import requests

# إعداد المعلومات الأساسية
TOKEN = "7960611747:AAF__2eag5N3R-5tLiy6Myq3rrNUOqzelWk"  # التوكن الخاص بالبوت
CHANNEL_LINK = "https://t.me/+xUCQE-w8QCszZTAy"  # رابط القناة للاشتراك الإجباري
REFERRAL_LINK = "https://t.me/DurovCapsBot/caps?startapp=374668608"  # رابط الإحالة
ADMIN_ID = "6169753913"  # معرف الأدمن

# قائمة المستخدمين الذين تم إخطار الأدمن عنهم
notified_users = set()

# وظيفة التحقق من الاشتراك
def is_user_subscribed(user_id):
    url = f"https://api.telegram.org/bot{TOKEN}/getChatMember?chat_id={CHANNEL_LINK}&user_id={user_id}"
    response = requests.get(url).json()
    status = response.get("result", {}).get("status", "")
    return status in ["member", "administrator", "creator"]

# وظيفة بدء البوت
async def start(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    user_name = update.effective_user.username or "Unknown"

    if not is_user_subscribed(user_id):
        # إذا لم يكن المستخدم مشتركًا، إرسال رسالة تطلب الاشتراك
        keyboard = [[InlineKeyboardButton("🔗 اضغط للاشتراك في القناة", url=CHANNEL_LINK)]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            "📢 **To continue using the bot, please subscribe to the channel.**\n\n"
            "1️⃣ Subscribe to the channel by clicking the button below.\n"
            "2️⃣ After subscribing, click /start to proceed.\n\n"
            "🌟 Join our community for the best services!\n\n"
            "📢 **لإكمال استخدام البوت، يرجى الاشتراك في القناة.**\n\n"
            "1️⃣ اشترك في القناة بالضغط على الزر أدناه.\n"
            "2️⃣ بعد الاشتراك، اضغط على /start لإكمال الاستخدام.\n\n"
            "🌟 كن جزءًا من مجتمعنا للحصول على أفضل الخدمات!",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
        return  # إنهاء الوظيفة إذا لم يكن المستخدم مشتركًا

    # إذا كان المستخدم مشتركًا، إرسال رسالة تحفيزية
    await update.message.reply_text(
        "🎉 **شكراً لاشتراكك!**\n\n"
        "🔗 **رابط الإحالة الخاص بك:**\n"
        f"{REFERRAL_LINK}\n\n"
        "📢 شارك الرابط مع أصدقائك لزيادة أرباحك!",
        parse_mode="Markdown"
    )
    await update.message.reply_text(
        "🎉 **Thank you for subscribing!**\n\n"
        "🔗 **Your referral link:**\n"
        f"{REFERRAL_LINK}\n\n"
        "📢 Share this link with your friends to boost your earnings!",
        parse_mode="Markdown"
    )

    # إرسال إشعار إلى الأدمن عند دخول مستخدم جديد لأول مرة
    if user_id not in notified_users:
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"🚨 مستخدم جديد دخل البوت لأول مرة:\n\nID: {user_id}\nUsername: @{user_name}"
        )
        notified_users.add(user_id)

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
