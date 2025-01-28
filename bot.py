from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackContext
import requests

# إعداد المعلومات الأساسية
TOKEN = "7960611747:AAF__2eag5N3R-5tLiy6Myq3rrNUOqzelWk"  # التوكن الخاص بالبوت
CHANNEL_ID = "+Sy18bATvBtg5ODgy"  # معرف القناة للاشتراك الإجباري
REFERRAL_LINK = "https://t.me/DurovCapsBot/caps?startapp=374668608"  # رابط الإحالة
ADMIN_ID = "6169753913"  # معرف الأدمن

# قائمة المستخدمين الذين تم إخطار الأدمن عنهم
notified_users = set()

# وظيفة التحقق من الاشتراك
def is_user_subscribed(user_id):
    url = f"https://api.telegram.org/bot{TOKEN}/getChatMember?chat_id={CHANNEL_ID}&user_id={user_id}"
    response = requests.get(url).json()
    status = response.get("result", {}).get("status", "")
    return status in ["member", "administrator", "creator"]

# وظيفة بدء البوت
def start(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    user_name = update.effective_user.username or "Unknown"

    if not is_user_subscribed(user_id):
        # إذا لم يكن المستخدم مشتركًا، إرسال رسالة تطلب الاشتراك
        keyboard = [[InlineKeyboardButton("اشترك الآن 📢", url=f"https://t.me/{CHANNEL_ID}")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(
            "مرحبًا! 🚀\nللاستفادة من خدمات البوت، يرجى الاشتراك في قناتنا أولاً. 👇",
            reply_markup=reply_markup
        )
    else:
        # إذا كان المستخدم مشتركًا، إرسال رسالة تحفيزية
        update.message.reply_text(
            f"🎉 شكرًا لاشتراكك!\n\nهيا ابدأ الربح الآن:\n{REFERRAL_LINK}"
        )

        # إرسال إشعار إلى الأدمن عند دخول مستخدم جديد لأول مرة
        if user_id not in notified_users:
            context.bot.send_message(
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
