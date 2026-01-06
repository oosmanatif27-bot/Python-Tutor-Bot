import os, telebot, threading, http.server, socketserver, time
from telebot import types

# التوكن حقك يا عثمان
TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = telebot.TeleBot(TOKEN)

# الدروس بالطريقة التعليمية اللي طلبتها يا عثمانوو 💡
lessons_data = {
    "1": {
        "title": "💡 الدرس 1: دالة print (الإخراج)",
        "explanation": "هي لسان البرمجة الذي يعرض النتائج. نستخدمها لإخراج المعلومات.\n• للنصوص (String): نضعها بين علامات تنصيص \" \".\n• للأرقام (Integer): نكتبها مباشرة بدون علامات.",
        "example": "print(\"المستوى\", 1)\n# دمجنا نص مع رقم",
        "exercise": "جرب تطبع اسمك 'Osman' وجنبه رقمك المفضل 7 في أمر واحد.",
        "solution": "print('Osman', 7)"
    },
    "2": {
        "title": "💡 الدرس 2: المتغيرات (Variables)",
        "explanation": "هي صناديق تخزن فيها البيانات ونعطيها اسم.\n• نكتب الاسم ثم علامة = ثم القيمة.",
        "example": "name = \"Osman\"\nscore = 10",
        "exercise": "عرف متغير باسم x وقيمته 50.",
        "solution": "x = 50"
    },
    "3": {
        "title": "💡 الدرس 3: العمليات الحسابية (Math)",
        "explanation": "بايثون شاطرة في الحساب!\n• الجمع (+)، الطرح (-)، الضرب (*)، القسمة (/).",
        "example": "total = 10 + (5 * 2)",
        "exercise": "احسب حاصل ضرب 5 في 4 واطبعه.",
        "solution": "print(5 * 4)"
    },
    "4": {
        "title": "💡 الدرس 4: دالة input (المدخلات)",
        "explanation": "تستخدم لسؤال المستخدم وطلب بيانات منه.\n• النص اللي داخل القوسين هو السؤال اللي يظهر للمستخدم.",
        "example": "age = input(\"كم عمرك؟ \")",
        "exercise": "اطلب من المستخدم إدخال اسمه وخزنه في متغير name.",
        "solution": "name = input('ما اسمك؟')"
    },
    "5": {
        "title": "💡 الدرس 5: القوائم (Lists)",
        "explanation": "صندوق واحد يحتوي على أشياء كثيرة مرتبة.\n• نستخدم الأقواس المربعة [ ] ونفصل بين العناصر بفاصلة.",
        "example": "colors = [\"أبيض\", \"وردي\"]",
        "exercise": "أنشئ قائمة باسم my_list فيها الأرقام 1، 2، 3.",
        "solution": "my_list = [1, 2, 3]"
    },
    "6": {
        "title": "💡 الدرس 6: القواميس (Dictionaries)",
        "explanation": "تخزن البيانات كزوج (مفتاح وقيمة).\n• نستخدم الأقواس { }، مثل اسم الطالب ورقمه.",
        "example": "user = {\"name\": \"Osman\", \"id\": 1}",
        "exercise": "أنشئ قاموس فيه المفتاح 'a' وقيمته 1.",
        "solution": "d = {'a': 1}"
    },
    "7": {
        "title": "💡 الدرس 7: الشروط (If Statement)",
        "explanation": "تخلي البرنامج يتخذ قرار بناءً على شرط.\n• إذا تحقق الشرط، ينفذ الكود المزاح (Indentation) تحتها.",
        "example": "if score > 50:\n    print(\"ناجح\")",
        "exercise": "اكتب شرط إذا كان x يساوي 10 اطبع 'صح'.",
        "solution": "if x == 10:\n    print('صح')"
    },
    "8": {
        "title": "💡 الدرس 8: التكرار (Loops)",
        "explanation": "تستخدم لتنفيذ الكود عدة مرات دون تكرار كتابته.\n• for تمر على عناصر محددة أو نطاق معين.",
        "example": "for i in range(3):\n    print(\"يقين\")",
        "exercise": "اطبع كلمة 'Hello' 5 مرات باستخدام for loop.",
        "solution": "for i in range(5):\n    print('Hello')"
    },
    "9": {
        "title": "💡 الدرس 9: الدوال (Functions)",
        "explanation": "تجميع كود في اسم واحد لاستدعائه لاحقاً.\n• نبدأ بكلمة def متبوعة باسم الدالة.",
        "example": "def say_hi():\n    print(\"هلا نينو\")",
        "exercise": "عرف دالة اسمها start تطبع 'بدأنا'.",
        "solution": "def start():\n    print('بدأنا')"
    },
    "10": {
        "title": "💡 الدرس 10: معالجة الأخطاء (Errors)",
        "explanation": "طريقة لمنع البرنامج من الانهيار عند حدوث خطأ.\n• try تحاول تنفيذ الكود، و except تعالج الخطأ.",
        "example": "try:\n    print(10/0)\nexcept:\n    print(\"خطأ حسابي\")",
        "exercise": "استخدم try لمنع خطأ تقسيم 5 على 0.",
        "solution": "try: 5/0\nexcept: pass"
    },
    "11": {
        "title": "💡 الدرس 11: التعامل مع الملفات (Files)",
        "explanation": "القدرة على قراءة أو كتابة بيانات داخل ملفات خارجية.\n• دالة open تستخدم لفتح الملف.",
        "example": "f = open(\"note.txt\", \"r\")",
        "exercise": "افتح ملف باسم 'data.txt' للقراءة فقط.",
        "solution": "open('data.txt', 'r')"
    },
    "12": {
        "title": "💡 الدرس 12: المكتبات (Modules)",
        "explanation": "استدعاء أدوات جاهزة لتوسيع قدرات برنامجك.\n• نستخدم import لإضافة المكتبة.",
        "example": "import math\nprint(math.sqrt(16))",
        "exercise": "استورد مكتبة time.",
        "solution": "import time"
    }
}

@bot.message_handler(commands=['start'])
def welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("قائمة الدروس")
    bot.send_message(message.chat.id, "🚀 البوت يعمل الآن يا نينو! اختر من القائمة:", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text == "قائمة الدروس")
def list_lessons(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    btns = [types.KeyboardButton(f"الدرس {i}") for i in range(1, 13)]
    markup.add(*btns)
    bot.send_message(message.chat.id, "📚 اختر الدرس الذي تريد تعلمه:", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text and m.text.startswith("الدرس "))
def handle_lesson(message):
    num = "".join(filter(str.isdigit, message.text))
    l = lessons_data.get(num, {})
    if l:
        text = f"*{l['title']}*\n\n{l['explanation']}\n\n💻 *مثال علمي:*\n`{l['example']}`"
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🎯 التحدي", callback_data=f"ex_{num}"))
        bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    data = call.data.split("_")
    l_id = data[1]
    l = lessons_data.get(l_id, {})
    if data[0] == "ex":
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🔑 الحل", callback_data=f"sol_{l_id}"))
        bot.edit_message_text(f"🎯 *التحدي:*\n{l['exercise']}", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
    elif data[0] == "sol":
        bot.edit_message_text(f"✅ *الحل:*\n`{l['solution']}`", call.message.chat.id, call.message.message_id, parse_mode="Markdown")

def run_health():
    try: socketserver.TCPServer(("", 8000), http.server.SimpleHTTPRequestHandler).serve_forever()
    except: pass

if __name__ == "__main__":
    threading.Thread(target=run_health, daemon=True).start()
    bot.remove_webhook() 
    time.sleep(1)
    print("🚀 Bot is Online!")
    bot.infinity_polling(skip_pending=True)

