from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackContext
import requests

# إعداد المعلومات الأساسية
TOKEN = "7960611747:AAF__2eag5N3R-5tLiy6Myq3rrNUOqzelWk"  # التوكن الخاص بالبوت
CHANNEL_LINK = "https://t.me/+xUCQE-w8QCszZTAy"  # رابط الدعوة للقناة
REFERRAL_LINK = "https://t.me/DurovCapsBot/caps?startapp=374668608"  # رابط الإحالة
ADMIN_ID = "6169753913"  # معرف الأدمن

# قائمة المستخدمين الذين تم إخطار الأدمن عنهم
notified_users = set()

# وظيفة التحقق من الاشتراك
def is_user_subscribed(user_id):
    # القناة خاصة، لذلك لا يمكن التحقق من الاشتراك باستخدام API
    # المستخدم يعتبر غير مشترك افتراضيًا إلا إذا طلب الانضمام
    return False

# وظيفة بدء البوت
async def start(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    user_name = update.effective_user.username or update.effective_user.first_name or "User"

    if not is_user_subscribed(user_id) and user_id not in notified_users:
        # إذا لم يكن المستخدم مشتركًا، إرسال رسالة تطلب الاشتراك باللغتين
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

    # إذا كان المستخدم مشتركًا، إرسال الرسالة مع الأزرار
    keyboard = [
        [InlineKeyboardButton("Let’s Go", url=REFERRAL_LINK)],
        [InlineKeyboardButton("Join the Channel", url=CHANNEL_LINK)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        f"Welcome aboard, {user_name}! ⭐️\n"
        "Is it just Caps, or something more?\n\n"
        "Earn tickets your way - tackle tasks or bring friends along!",
        reply_markup=reply_markup
    )

    # إرسال إشعار إلى الأدمن عند دخول مستخدم جديد لأول مرة
    if user_id not in notified_users:
        notified_users.add(user_id)
        total_users = len(notified_users)
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
