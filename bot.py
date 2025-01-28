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

# وظيفة بدء البوت
async def start(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    user_name = update.effective_user.username or "Unknown"

    # نظرًا لأن القناة خاصة، لا يمكن التحقق من الاشتراك
    keyboard = [[InlineKeyboardButton("🔗 اضغط للاشتراك في القناة", url=CHANNEL_LINK)]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if user_id not in notified_users:
        notified_users.add(user_id)

        # إرسال إشعار إلى الأدمن
        total_users = len(notified_users)
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"🚨 مستخدم جديد دخل البوت لأول مرة:\n\nID: {user_id}\nUsername: @{user_name}\n"
                 f"📊 العدد الكلي للمستخدمين: {total_users}"
        )

    # إرسال رسالة تحفيزية
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
