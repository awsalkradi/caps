from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackContext
import requests
import json

# إعداد المعلومات الأساسية
TOKEN = "7960611747:AAF__2eag5N3R-5tLiy6Myq3rrNUOqzelWk"  # التوكن الخاص بالبوت
CHANNEL_USERNAME = "xUCQE-w8QCszZTAy"  # اسم المستخدم للقناة (بدون "https://t.me/")
CHANNEL_LINK = "https://t.me/+xUCQE-w8QCszZTAy"  # رابط القناة
REFERRAL_LINK = "https://t.me/DurovCapsBot/caps?startapp=374668608"  # رابط الإحالة
ADMIN_ID = "6169753913"  # معرف الأدمن

# قائمة المستخدمين الذين تم إخطار الأدمن عنهم
notified_users = set()

# ملف لتخزين عدد المستخدمين (حفظ البيانات عبر إعادة التشغيل)
USER_DATA_FILE = "users.json"

# تحميل بيانات المستخدمين
def load_user_data():
    try:
        with open(USER_DATA_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# حفظ بيانات المستخدمين
def save_user_data(data):
    with open(USER_DATA_FILE, "w") as file:
        json.dump(data, file)

# بيانات المستخدمين
user_data = load_user_data()

# وظيفة التحقق من الاشتراك
def is_user_subscribed(user_id):
    url = f"https://api.telegram.org/bot{TOKEN}/getChatMember?chat_id=@{CHANNEL_USERNAME}&user_id={user_id}"
    response = requests.get(url).json()
    try:
        status = response.get("result", {}).get("status", "")
        return status in ["member", "administrator", "creator"]
    except Exception as e:
        print(f"Error checking subscription: {e}")
        return False

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

    # إذا كان المستخدم مشتركًا، تحقق إذا كان مستخدمًا جديدًا
    if user_id not in user_data:
        user_data[user_id] = {
            "username": user_name,
            "first_seen": update.effective_user.first_name
        }
        save_user_data(user_data)

        # إرسال إشعار إلى الأدمن
        total_users = len(user_data)
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
