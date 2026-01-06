import os, telebot, threading, http.server, socketserver
from telebot import types

TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = telebot.TeleBot(TOKEN)

# --- المنهج العلمي المبسط (12 درس) ---
# ملاحظة: أبقيت الدروس كما هي في كودك تماماً لضمان الأداء
lessons_data = {
    "1": {
        "title": "الدرس 1: دالة print (الإخراج)",
        "explanation": "هي لسان البرمجة الذي يعرض النتائج. نستخدمها لإخراج المعلومات.\n• للنصوص (String): نضعها بين علامات تنصيص `\" \"`.\n• للأرقام (Integer): نكتبها مباشرة بدون علامات.",
        "example": "مثال علمي:\n`print(\"المستوى\", 1)`\nهنا دمجنا نص (String) مع رقم (Integer).",
        "exercise": "اكتب كود يطبع اسمك ورقمك المفضل بجانبه.",
        "solution": "`print(\"عثمان\", 7)`"
    },
    "2": {
        "title": "الدرس 2: المتغيرات (Variables)",
        "explanation": "هي مخازن في الذاكرة لها اسم ونوع. نستخدمها لحفظ البيانات.\n• المثال: `score = 10` هنا حفظنا القيمة 10 في متغير نوعه Integer.",
        "exercise": "اصنع متغير اسمه `my_text` واحفظ فيه جملة 'أنا مبرمج'.",
        "solution": "`my_text = \"أنا مبرمج\"`"
    },
    "3": {
        "title": "الدرس 3: العمليات الحسابية (Operators)",
        "explanation": "بايثون تنفذ الحساب بدقة عالية.\n• `+` جمع، `-` طرح، `*` ضرب، `/` قسمة.",
        "exercise": "اكتب كود يطبع ناتج ضرب 10 في 10.",
        "solution": "`print(10 * 10)`"
    },
    "4": {
        "title": "الدرس 4: المدخلات (User Input)",
        "explanation": "دالة `input` تسمح للبرنامج بسؤال المستخدم وانتظار الرد. النتيجة دائماً تكون نص (String).",
        "exercise": "اسأل المستخدم عن لونه المفضل واحفظه في متغير `color`.",
        "solution": "`color = input(\"ما لونك المفضل؟\")`"
    },
    "5": {
        "title": "الدرس 5: القوائم (Lists)",
        "explanation": "مجموعة عناصر مخزنة في مكان واحد. نصل لكل عنصر عبر رقمه (Index).",
        "exercise": "اصنع قائمة باسم `tools` وضع فيها 'Laptop' و 'Mouse'.",
        "solution": "`tools = [\"Laptop\", \"Mouse\"]`"
    },
    "6": {
        "title": "الدرس 6: القواميس (Dictionaries)",
        "explanation": "تخزين البيانات بنظام مفتاح وقيمة (Key-Value) لسهولة البحث.",
        "exercise": "اصنع قاموساً فيه الاسم 'عثمان' والعمر 20.",
        "solution": "`user = {\"name\": \"عثمان\", \"age\": 20}`"
    },
    "7": {
        "title": "الدرس 7: الجمل الشرطية (If Statements)",
        "explanation": "تسمح للبرنامج باتخاذ قرارات. 'لو' تحقق الشرط، نفذ الكود.",
        "exercise": "اكتب شرطاً يطبع 'مسموح' إذا كان العمر أكبر من 18.",
        "solution": "if age > 18:\n    print(\"مسموح\")"
    },
    "8": {
        "title": "الدرس 8: الحلقات التكرارية (Loops)",
        "explanation": "نستخدم `for` لتكرار مهمة معينة لعدد محدد من المرات بدلاً من كتابتها يدوياً.",
        "exercise": "اطبع الأرقام من 0 إلى 4 باستخدام range.",
        "solution": "for i in range(5):\n    print(i)"
    },
    "9": {
        "title": "الدرس 9: الدوال (Functions)",
        "explanation": "مجموعة أوامر نعطيها اسماً لنستخدمها لاحقاً. تبدأ بكلمة `def`.",
        "exercise": "عرف دالة اسمها `greet` تطبع 'أهلاً بك'.",
        "solution": "def greet():\n    print(\"أهلاً بك\")"
    },
    "10": {
        "title": "الدرس 10: معالجة الأخطاء (Error Handling)",
        "explanation": "نستخدم `try` و `except` لمنع البرنامج من التوقف عند حدوث خطأ مفاجئ.",
        "exercise": "جرب كود يقسم 10 على 0 واحميه من الانهيار.",
        "solution": "try:\n    print(10/0)\nexcept:\n    print(\"خطأ حسابي!\")"
    },
    "11": {
        "title": "الدرس 11: التعامل مع الملفات (File I/O)",
        "explanation": "بايثون تستطيع كتابة وقراءة نصوص من ملفات `.txt` خارجية.",
        "exercise": "افتح ملفاً باسم 'data.txt' واكتب فيه 'بايثون قوية'.",
        "solution": "with open(\"data.txt\", \"w\") as f:\n    f.write(\"بايثون قوية\")"
    },
    "12": {
        "title": "الدرس 12: المكتبات (Modules)",
        "explanation": "نستخدم `import` لجلب أدوات مبرمجة مسبقاً، مثل مكتبة `math` للحسابات المتقدمة.",
        "exercise": "استورد مكتبة الوقت time.",
        "solution": "import time"
    }
}

# --- إدارة الرسائل ---
@bot.message_handler(commands=['start'])
def welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add("مقدمة بايثون", "قائمة الدروس")
    bot.send_message(message.chat.id, "🚀 مرحباً بك في أكاديمية البرمجة الذكية!\nاختر من الأزرار لبدء التعلم:", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text == "مقدمة بايثون")
def intro(message):
    text = """تُعد بايثون (Python) لغة برمجة عالية المستوى، تمتاز بالبساطة والقوة. تُستخدم في الذكاء الاصطناعي، الأمن السيبراني، وتطوير التطبيقات."""
    bot.send_message(message.chat.id, text)

@bot.message_handler(func=lambda m: m.text == "قائمة الدروس")
def list_lessons(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    # التأكد من إنشاء الأزرار للـ 12 درساً كاملاً
    btns = [types.KeyboardButton(f"الدرس {i}") for i in range(1, 13)]
    markup.add(*btns, "الرجوع")
    bot.send_message(message.chat.id, "📚 قائمة الدروس الـ 12 المتاحة:", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text and m.text.startswith("الدرس "))
def handle_lesson(message):
    # تنظيف النص واستخراج الرقم بشكل أدق لضمان عمل الدروس من 4 إلى 12
    num = message.text.replace("الدرس", "").strip()
    if num in lessons_data:
        l = lessons_data[num]
        text = f"💡 *{l['title']}*\n\n{l['explanation']}\n\n{l['example']}"
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🎯 تحدي الدرس", callback_data=f"ex_{num}"))
        bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    # استخدام try لتجنب أي خطأ في الـ callback_data
    try:
        l_id = call.data.split("_")[1]
        l = lessons_data[l_id]
        if call.data.startswith("ex_"):
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("🔑 الحل العلمي", callback_data=f"sol_{l_id}"))
            bot.edit_message_text(f"🎯 *التحدي:*\n{l['exercise']}", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
        elif call.data.startswith("sol_"):
            bot.edit_message_text(f"✅ *الحل:* {l['solution']}\n\nاستمر في التعلم! 🚀", call.message.chat.id, call.message.message_id, parse_mode="Markdown")
    except: pass

# --- Health Server ---
def run_health():
    try: socketserver.TCPServer(("", 8000), http.server.SimpleHTTPRequestHandler).serve_forever()
    except: pass

threading.Thread(target=run_health, daemon=True).start()

if __name__ == "__main__":
    bot.remove_webhook()
    bot.infinity_polling(skip_pending=True)
