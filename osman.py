import os, telebot, threading, http.server, socketserver, time
from telebot import types

# التوكن (تأكد من وضعه في إعدادات Koyeb)
TOKEN = os.getenv("TELEGRAM_TOKEN2")
bot = telebot.TeleBot(TOKEN)

# تتبع استهبال المستخدمين
user_warnings = {}

# بيانات دروس C++
lessons_data = {
    "1": {
        "title": "🚀 الدرس 1: الهيكل الأساسي ودالة cout",
        "explanation": "في C++ نستخدم <code>cout</code> للطباعة. ولا تنسَ الفاصلة المنقوطة <code>;</code> في نهاية كل أمر.",
        "example": "#include <iostream>\nusing namespace std;\n\nint main() {\n  cout << 'Hello World';\n  return 0;\n}",
        "exercise": "اطبع 'C++ is Power' باستخدام cout.",
        "solution": "cout << 'C++ is Power';"
    },
    "2": {
        "title": "📦 الدرس 2: المتغيرات Variables",
        "explanation": "لازم تحدد النوع: <code>int</code> للرقم، <code>string</code> للنص.",
        "example": "int x = 10;\nstring dev = 'Osman';",
        "exercise": "عرف متغير نصي اسمه name وقيمته 'Bot'.",
        "solution": "string name = 'Bot';"
    }
}

@bot.message_handler(commands=['start'])
def welcome(message):
    user_warnings[message.chat.id] = 0 # تصفير العداد عند البداية
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("📚 قائمة دروس C++")
    bot.send_message(message.chat.id, "👋 مرحباً بك! لا تضيع وقتك واضغط على الزر تحت:", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text == "📚 قائمة دروس C++")
def list_lessons(message):
    user_warnings[message.chat.id] = 0
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    btns = [types.KeyboardButton(f"الدرس {i}") for i in range(1, 3)]
    markup.add(*btns)
    bot.send_message(message.chat.id, "اختر الدرس يا وحش:", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text and m.text.startswith("الدرس "))
def handle_lesson(message):
    user_warnings[message.chat.id] = 0
    num = "".join(filter(str.isdigit, message.text))
    l = lessons_data.get(num)
    if l:
        text = f"<b>{l['title']}</b>\n\n📖 <b>الشرح:</b>\n{l['explanation']}\n\n💻 <b>مثال:</b>\n<code>{l['example']}</code>"
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🎯 التحدي", callback_data=f"ex_{num}"))
        bot.send_message(message.chat.id, text, parse_mode="HTML", reply_markup=markup)

# معالج الرسائل العشوائية (نظام التحجير)
@bot.message_handler(func=lambda m: True)
def handle_random_messages(message):
    user_id = message.chat.id
    count = user_warnings.get(user_id, 0) + 1
    user_warnings[user_id] = count

    if count == 1:
        bot.reply_to(message, "وش تهبل اختر من الازرار ي ورع 😤")
    elif count == 2:
        bot.reply_to(message, "الازرار ياخي م افهمك اضغط بالازرار 😠")
    else:
        bot.reply_to(message, "يا مريض شكلك تبغا الAi هاذ بوت AI ادخل له لو محتاج مساعدة @Botneno_Aibot 🙄")

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    try:
        data = call.data.split("_")
        action, l_id = data[0], data[1]
        l = lessons_data.get(l_id)
        if l:
            if action == "ex":
                markup = types.InlineKeyboardMarkup()
                markup.add(types.InlineKeyboardButton("🔑 الحل", callback_data=f"sol_{l_id}"))
                bot.edit_message_text(f"🎯 <b>التحدي:</b>\n{l['exercise']}", call.message.chat.id, call.message.message_id, parse_mode="HTML", reply_markup=markup)
            elif action == "sol":
                bot.edit_message_text(f"✅ <b>الحل:</b>\n<code>{l['solution']}</code>", call.message.chat.id, call.message.message_id, parse_mode="HTML")
    except Exception as e:
        print(f"Callback Error: {e}")

# سيرفر الحماية لـ Koyeb
def run_health():
    class Handler(http.server.SimpleHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Bot is Alive")

    try:
        with socketserver.TCPServer(("", 8000), Handler) as httpd:
            httpd.serve_forever()
    except: pass

if __name__ == "__main__":
    threading.Thread(target=run_health, daemon=True).start()
    print("🚀 C++ Bot Started Successfully!")
    
    # محرك التشغيل اللانهائي (مضاد للتوقف)
    while True:
        try:
            bot.infinity_polling(skip_pending=True, timeout=10, long_polling_timeout=5)
        except Exception as e:
            print(f"Bot Polling Error: {e}")
            time.sleep(5) # انتظر 5 ثواني وارجع اشتغل تلقائياً