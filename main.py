import os, telebot, threading, http.server, socketserver, time
from telebot import types

# جلب التوكن - تأكد أنه مضاف في Settings -> Variables في كويب باسم TELEGRAM_TOKEN
TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = telebot.TeleBot(TOKEN)

# --- المنهج العلمي المكتمل (12 درس - تم فحص كل المفاتيح) ---
lessons_data = {
    "1": {
        "title": "الدرس 1: دالة print",
        "explanation": "هي لسان الكمبيوتر، نستخدمها لنعرض النصوص (String) بين `\" \"` أو الأرقام (Integer) مباشرة.",
        "example": "print(\"عثمان\", 1)",
        "exercise": "اطبع اسمك ورقم 5 بجانبه.",
        "solution": "print(\"عثمان\", 5)"
    },
    "2": {
        "title": "الدرس 2: المتغيرات Variables",
        "explanation": "صندوق في الذاكرة له 'اسم' نخزن فيه 'قيمة'.",
        "example": "score = 100",
        "exercise": "خزن نص 'بايثون' في متغير اسمه a.",
        "solution": "a = \"بايثون\""
    },
    "3": {
        "title": "الدرس 3: الحساب Math",
        "explanation": "بايثون آلة حاسبة ذكية تستخدم `+ - * /`.",
        "example": "print(10 * 2)",
        "exercise": "اجمع 50 مع 50 واطبع الناتج.",
        "solution": "print(50 + 50)"
    },
    "4": {
        "title": "الدرس 4: المدخلات Input",
        "explanation": "دالة `input` تجعل الكمبيوتر ينتظر منك كلاماً (String).",
        "example": "x = input(\"ما اسمك؟\")",
        "exercise": "اسأل المستخدم عن عمره وخزنه في متغير age.",
        "solution": "age = input(\"كم عمرك؟\")"
    },
    "5": {
        "title": "الدرس 5: القوائم Lists",
        "explanation": "حقيبة تجمع عناصر كثيرة، ونبدأ العد فيها من الرقم 0.",
        "example": "my_list = [1, 2, 3]",
        "exercise": "اصنع قائمة فيها 'خالد' و 'سارة'.",
        "solution": "names = [\"خالد\", \"سارة\"]"
    },
    "6": {
        "title": "الدرس 6: القواميس Dictionaries",
        "explanation": "خزانة معلومات تعمل بنظام (مفتاح : قيمة).",
        "example": "user = {\"name\": \"عثمان\"}",
        "exercise": "اصنع قاموساً فيه المفتاح 'city' والقيمة 'Riyadh'.",
        "solution": "d = {\"city\": \"Riyadh\"}"
    },
    "7": {
        "title": "الدرس 7: الشروط If",
        "explanation": "بوابة القرار؛ ينفذ الكود فقط إذا كان الشرط صحيحاً (True).",
        "example": "if x > 5: print(\"كبير\")",
        "exercise": "اكتب شرطاً يطبع 'نجاح' إذا كانت الدرجة (grade) تساوي 100.",
        "solution": "if grade == 100: print(\"نجاح\")"
    },
    "8": {
        "title": "الدرس 8: التكرار Loops",
        "explanation": "تكرار الكود آلياً بدلاً من كتابته مئة مرة.",
        "example": "for i in range(3): print(\"هلا\")",
        "exercise": "اطبع الأرقام من 0 إلى 4.",
        "solution": "for i in range(5): print(i)"
    },
    "9": {
        "title": "الدرس 9: الدوال Functions",
        "explanation": "مصنع صغير للكود نعطيه اسماً لنستخدمه متى شئنا.",
        "example": "def hello(): print(\"أهلاً\")",
        "exercise": "عرف دالة اسمها start تطبع كلمة 'ابدأ'.",
        "solution": "def start(): print(\"ابدأ\")"
    },
    "10": {
        "title": "الدرس 10: الأخطاء Errors",
        "explanation": "نستخدم `try` لتجربة الكود و `except` لمنع البرنامج من التحطم إذا وجد خطأ.",
        "example": "try: print(1/0)\nexcept: print(\"خطأ!\")",
        "exercise": "ضع كود `print(x)` داخل try (بافتراض x غير موجود).",
        "solution": "try: print(x)\nexcept: print(\"غير موجود\")"
    },
    "11": {
        "title": "الدرس 11: الملفات Files",
        "explanation": "بايثون تستطيع فتح وقراءة ملفات النصوص الخارجية.",
        "example": "f = open(\"test.txt\", \"r\")",
        "exercise": "افتح ملفاً للكتابة اسم 'note.txt'.",
        "solution": "f = open(\"note.txt\", \"w\")"
    },
    "12": {
        "title": "الدرس 12: المكتبات Modules",
        "explanation": "أدوات جاهزة صنعها مبرمجون آخرون لنستخدمها بكلمة `import`.",
        "example": "import math\nprint(math.sqrt(16))",
        "exercise": "استورد مكتبة الوقت time.",
        "solution": "import time"
    }
}

# --- إدارة الرسائل ---

@bot.message_handler(commands=['start'])
def welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add("مقدمة بايثون", "قائمة الدروس")
    bot.send_message(message.chat.id, "🚀 تم تحديث النظام! اختر من القائمة أدناه:", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text == "قائمة الدروس")
def list_lessons(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    btns = [types.KeyboardButton(f"الدرس {i}") for i in range(1, 13)]
    markup.add(*btns, "الرجوع")
    bot.send_message(message.chat.id, "📚 اختر درساً (من 1 إلى 12):", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text and m.text.startswith("الدرس "))
def handle_lesson(message):
    # استخراج الرقم لضمان عدم حدوث خطأ في البحث داخل القاموس
    num = "".join(filter(str.isdigit, message.text))
    if num in lessons_data:
        l = lessons_data[num]
        # بناء الرسالة مع التأكد من وجود كل الحقول
        text = f"💡 *{l['title']}*\n\n📖 *الشرح:* {l['explanation']}\n\n💻 *مثال علمي:*\n`{l['example']}`"
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🎯 تحدي الدرس", callback_data=f"ex_{num}"))
        bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    data = call.data.split("_")
    action = data[0]
    l_id = data[1]
    l = lessons_data[l_id]
    
    if action == "ex":
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🔑 الحل العلمي", callback_data=f"sol_{l_id}"))
        bot.edit_message_text(f"🎯 *تحدي الدرس {l_id}:*\n{l['exercise']}", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
    elif action == "sol":
        bot.edit_message_text(f"✅ *الحل البرمجي الصحيح:*\n`{l['solution']}`\n\nاستمر يا بطل! 🚀", call.message.chat.id, call.message.message_id, parse_mode="Markdown")

# --- تشغيل السيرفر الصحي ---
def run_health():
    try: socketserver.TCPServer(("", 8000), http.server.SimpleHTTPRequestHandler).serve_forever()
    except: pass

if __name__ == "__main__":
    threading.Thread(target=run_health, daemon=True).start()
    # تنظيف الاتصال لتجنب Conflict 409
    bot.remove_webhook()
    time.sleep(1)
    print("✅ البوت متصل الآن ومستعد لجميع الدروس!")
    bot.infinity_polling(skip_pending=True)
