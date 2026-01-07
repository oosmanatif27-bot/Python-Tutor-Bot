import os, telebot, threading, http.server, socketserver, time
from telebot import types

# جلب التوكن من إعدادات Koyeb
TOKEN = os.getenv("TELEGRAM_TOKEN2")
bot = telebot.TeleBot(TOKEN)

# تتبع التنبيهات
user_warnings = {}

# قاعدة بيانات الدروس الـ 14 (النمط: شرح -> مثال -> تحدي -> حل)
lessons_data = {
    "1": {
        "title": "🏛️ الدرس 1: هيكل البرنامج",
        "explanation": "يتكون برنامج C++ الأساسي من تضمين المكتبات ودالة main التي تعتبر نقطة الانطلاق.",
        "example": "#include <iostream>\nusing namespace std;\n\nint main() {\n    return 0;\n}",
        "exercise": "اكتب الهيكل الأساسي لبرنامج C++.",
        "solution": "#include <iostream>\nusing namespace std;\nint main() { return 0; }"
    },
    "2": {
        "title": "📥 الدرس 2: الطباعة والإدخال",
        "explanation": "نستخدم cout لطباعة البيانات و cin لاستقبال المدخلات من المستخدم.",
        "example": "int x;\ncout << 'Enter: ';\ncin >> x;",
        "exercise": "اكتب أمراً لاستقبال قيمة في متغير اسمه age.",
        "solution": "cin >> age;"
    },
    "3": {
        "title": "📦 الدرس 3: أنواع البيانات",
        "explanation": "تحدد أنواع البيانات حجم الذاكرة المحجوزة، مثل int للأرقام و bool للقيم المنطقية.",
        "example": "int n = 5;\nbool status = true;",
        "exercise": "عرف متغير منطقي باسم isOpen وقيمته true.",
        "solution": "bool isOpen = true;"
    },
    "4": {
        "title": "➗ الدرس 4: العمليات الحسابية",
        "explanation": "تشمل العمليات الأساسية، وأهمها باقي القسمة % الذي يستخدم كثيراً في التشفير.",
        "example": "int r = 10 % 3; // الناتج 1",
        "exercise": "احسب باقي قسمة 20 على 6.",
        "solution": "int res = 20 % 6;"
    },
    "5": {
        "title": "⚖️ الدرس 5: الجمل الشرطية",
        "explanation": "تستخدم if و else و switch لاتخاذ قرارات منطقية بناءً على شروط معينة.",
        "example": "if (x == 1) { cout << 'One'; }",
        "exercise": "اكتب شرطاً يتأكد إذا كان x يساوي 10.",
        "solution": "if (x == 10) { }"
    },
    "6": {
        "title": "🔄 الدرس 6: الحلقات التكرارية",
        "explanation": "تستخدم for و while لتكرار العمليات، وهي أساسية في فحص البيانات (Scanning).",
        "example": "for(int i=0; i<3; i++) { }",
        "exercise": "اكتب حلقة for تبدأ من 0 وتنتهي عند 5.",
        "solution": "for(int i=0; i<5; i++) { }"
    },
    "7": {
        "title": "📊 الدرس 7: المصفوفات",
        "explanation": "المصفوفة تخزن عناصر متعددة من نفس النوع في أماكن متجاورة بالذاكرة.",
        "example": "int arr[3] = {1, 2, 3};",
        "exercise": "عرف مصفوفة أرقام حجمها 10 عناصر.",
        "solution": "int arr[10];"
    },
    "8": {
        "title": "🔤 الدرس 8: النصوص (Strings)",
        "explanation": "نستخدم مكتبة string للتعامل مع النصوص والجمل البرمجية بشكل مرن.",
        "example": "string s = 'Cyber';",
        "exercise": "عرف نصاً باسم msg وقيمته 'Hello'.",
        "solution": "string msg = 'Hello';"
    },
    "9": {
        "title": "⚙️ الدرس 9: الدوال (Functions)",
        "explanation": "الدوال تساعد في تقسيم الكود إلى أجزاء صغيرة منظمة وقابلة لإعادة الاستخدام.",
        "example": "void test() { }",
        "exercise": "عرف دالة باسم start نوعها void.",
        "solution": "void start() { }"
    },
    "10": {
        "title": "🎯 الدرس 10: المؤشرات (Pointers)",
        "explanation": "المؤشر يخزن عنوان الذاكرة. فهمه ضروري جداً لمختصي الأمن لفهم ثغرات الذاكرة.",
        "example": "int* p = &x;",
        "exercise": "عرف مؤشر ptr يشير لمتغير int.",
        "solution": "int* ptr;"
    },
    "11": {
        "title": "🔗 الدرس 11: المراجع (References)",
        "explanation": "المرجع هو اسم مستعار لمتغير موجود، ويستخدم غالباً في تمرير البيانات للدوال بكفاءة.",
        "example": "int &ref = x;",
        "exercise": "عرف مرجعاً r للمتغير val.",
        "solution": "int &r = val;"
    },
    "12": {
        "title": "🧠 الدرس 12: إدارة الذاكرة",
        "explanation": "استخدام new و delete لحجز ومسح الذاكرة يدوياً، وهو ما يسمى Heap Management.",
        "example": "int* p = new int; delete p;",
        "exercise": "احجز مساحة ديناميكية لرقم صحيح باستخدام new.",
        "solution": "int* p = new int;"
    },
    "13": {
        "title": "🏗️ الدرس 13: الهياكل (Structs)",
        "explanation": "تسمح Struct بتجميع أنواع بيانات مختلفة في كيان واحد منظم.",
        "example": "struct Data { int id; };",
        "exercise": "عرف هيكلاً باسم Info يحتوي على متغير int.",
        "solution": "struct Info { int x; };"
    },
    "14": {
        "title": "💎 الدرس 14: الأصناف (Classes)",
        "explanation": "أساس البرمجة الكائنية (OOP)، حيث تجمع البيانات والوظائف في كائن واحد.",
        "example": "class App { public: int id; };",
        "exercise": "عرف كلاًساً بسيطاً باسم User.",
        "solution": "class User { };"
    }
}

# --- منطق عمل البوت ---

@bot.message_handler(commands=['start'])
def welcome(message):
    user_warnings[message.chat.id] = 0
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("📚 قائمة دروس C++")
    bot.send_message(message.chat.id, "👋 مرحباً بك في الدورة الشاملة.\n\nالرجاء اختيار 'قائمة الدروس' للبدء:", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text == "📚 قائمة دروس C++")
def list_lessons(message):
    user_warnings[message.chat.id] = 0
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btns = [types.KeyboardButton(f"الدرس {i}") for i in lessons_data.keys()]
    markup.add(*btns)
    bot.send_message(message.chat.id, "اختر الدرس المطلوب:", reply_markup=markup)

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

@bot.message_handler(func=lambda m: True)
def handle_random(message):
    user_id = message.chat.id
    count = user_warnings.get(user_id, 0) + 1
    user_warnings[user_id] = count
    if count == 1:
        bot.reply_to(message, "⚠️ يرجى استخدام الأزرار المخصصة فقط.")
    elif count == 2:
        bot.reply_to(message, "🚫 البوت مخصص للدروس التعليمية، استخدم القائمة.")
    else:
        bot.reply_to(message, "🤖 للمساعدة المتقدمة تواصل مع: @Botneno_Aibot")

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    try:
        action, l_id = call.data.split("_")
        l = lessons_data.get(l_id)
        if l:
            if action == "ex":
                markup = types.InlineKeyboardMarkup()
                markup.add(types.InlineKeyboardButton("🔑 الحل", callback_data=f"sol_{l_id}"))
                bot.edit_message_text(f"🎯 <b>التحدي:</b>\n{l['exercise']}", call.message.chat.id, call.message.message_id, parse_mode="HTML", reply_markup=markup)
            elif action == "sol":
                bot.edit_message_text(f"✅ <b>الحل:</b>\n<code>{l['solution']}</code>", call.message.chat.id, call.message.message_id, parse_mode="HTML")
    except: pass

# --- الحماية والتشغيل ---
def run_health():
    class Handler(http.server.SimpleHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Alive")
    try:
        with socketserver.TCPServer(("", 8000), Handler) as httpd:
            httpd.serve_forever()
    except: pass

if __name__ == "__main__":
    threading.Thread(target=run_health, daemon=True).start()
    bot.remove_webhook()
    time.sleep(1)
    print("🚀 Bot is Online!")
    while True:
        try:
            bot.infinity_polling(skip_pending=True)
        except:
            time.sleep(5)
