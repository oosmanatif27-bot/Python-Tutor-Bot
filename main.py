import os, telebot, threading, http.server, socketserver, time
from telebot import types

# --- إعدادات التوكنات من Koyeb ---
TOKEN_PY = os.getenv("TELEGRAM_TOKEN")   
TOKEN_CPP = os.getenv("TELEGRAM_TOKEN2") 

bot_py = telebot.TeleBot(TOKEN_PY)
bot_cpp = telebot.TeleBot(TOKEN_CPP)

# --- قاعدة بيانات دروس بايثون (12 درس) ---
lessons_py = {
    "1": {"title": "الدرس 1: دالة print 💡", "explanation": "عرض النتائج على الشاشة.", "example": "print('Hello World')", "exercise": "اطبع اسمك باستخدام بايثون.", "solution": "print('Osman')"},
    "2": {"title": "الدرس 2: المتغيرات 💡", "explanation": "تخزين البيانات في ذاكرة البرنامج.", "example": "x = 5\nname = 'Osman'", "exercise": "عرف متغير x وقيمته 100.", "solution": "x = 100"},
    "3": {"title": "الدرس 3: العمليات الحسابية 💡", "explanation": "الجمع (+)، الطرح (-)، الضرب (*)، القسمة (/).", "example": "result = 10 * 2", "exercise": "احسب حاصل جمع 5 و 15 واطبعه.", "solution": "print(5 + 15)"},
    "4": {"title": "الدرس 4: دالة input 💡", "explanation": "استقبال البيانات من المستخدم.", "example": "age = input('Enter your age: ')", "exercise": "اطلب من المستخدم إدخال لونه المفضل.", "solution": "color = input('What is your color? ')"},
    "5": {"title": "الدرس 5: القوائم Lists 💡", "explanation": "تخزين عدة قيم في متغير واحد.", "example": "tools = ['Python', 'C++']", "exercise": "أنشئ قائمة فيها الأرقام 1 و 2.", "solution": "numbers = [1, 2]"},
    "6": {"title": "الدرس 6: القواميس Dictionaries 💡", "explanation": "تخزين البيانات بنظام (مفتاح: قيمة).", "example": "user = {'id': 1, 'name': 'Osman'}", "exercise": "أنشئ قاموساً يحتوي على 'city' وقيمتها 'Dubai'.", "solution": "d = {'city': 'Dubai'}"},
    "7": {"title": "الدرس 7: الشروط If Statement 💡", "explanation": "تنفيذ كود معين بناءً على شرط.", "example": "if x > 10:\n    print('Big')", "exercise": "اكتب شرطاً يطبع 'Success' إذا كان x يساوي 10.", "solution": "if x == 10:\n    print('Success')"},
    "8": {"title": "الدرس 8: التكرار Loops 💡", "explanation": "تنفيذ الكود لعدد معين من المرات.", "example": "for i in range(5):\n    print(i)", "exercise": "اطبع كلمة 'Hello' ثلاث مرات.", "solution": "for i in range(3):\n    print('Hello')"},
    "9": {"title": "الدرس 9: الدوال Functions 💡", "explanation": "تجميع الكود لإعادة استخدامه.", "example": "def greet():\n    print('Hi')", "exercise": "عرف دالة باسم my_func تطبع 'Hi'.", "solution": "def my_func():\n    print('Hi')"},
    "10": {"title": "الدرس 10: معالجة الأخطاء 💡", "explanation": "منع البرنامج من الانهيار عند حدوث خطأ.", "example": "try:\n    x = 1/0\nexcept: print('Error')", "exercise": "استخدم try لمنع خطأ تقسيم 5 على 0.", "solution": "try: 5/0\nexcept: pass"},
    "11": {"title": "الدرس 11: الملفات 💡", "explanation": "فتح وقراءة الملفات النصية.", "example": "f = open('data.txt', 'r')", "exercise": "افتح ملفاً باسم test.txt للقراءة.", "solution": "open('test.txt', 'r')"},
    "12": {"title": "الدرس 12: المكتبات Modules 💡", "explanation": "استخدام أدوات برمجية جاهزة.", "example": "import math\nprint(math.sqrt(16))", "exercise": "استورد مكتبة time.", "solution": "import time"}
}

# --- قاعدة بيانات دروس C++ (14 درس) ---
lessons_cpp = {
    "1": {"title": "🏛️ 1: الهيكل الأساسي", "explanation": "المكتبات ودالة main هي نقطة البداية.", "example": "#include <iostream>\nint main() { return 0; }", "exercise": "اكتب هيكل دالة main.", "solution": "int main() { }"},
    "2": {"title": "📥 2: الطباعة والإدخال", "explanation": "استخدام cout للطباعة و cin للإدخال.", "example": "cout << x;\ncin >> y;", "exercise": "اطبع كلمة 'Welcome'.", "solution": "cout << 'Welcome';"},
    "3": {"title": "📦 3: أنواع البيانات", "explanation": "int (رقم)، float (كسر)، string (نص).", "example": "int x = 5;\nstring name = 'Ali';", "exercise": "عرف متغيراً نصياً باسم s.", "solution": "string s;"},
    "4": {"title": "➗ 4: العمليات الحسابية", "explanation": "نفس بايثون مع أهمية الفاصلة المنقوطة ;", "example": "int x = 5 + 5;", "exercise": "اضرب 5 في 10.", "solution": "int x = 5 * 10;"},
    "5": {"title": "⚖️ 5: الجمل الشرطية", "explanation": "استخدام if و else للقرار.", "example": "if(x == 1) { }", "exercise": "شرط إذا كان x أكبر من 0.", "solution": "if(x > 0) { }"},
    "6": {"title": "🔄 6: الحلقات (Loops)", "explanation": "for, while, do-while.", "example": "for(int i=0; i<5; i++)", "exercise": "حلقة تكرار تبدأ من 0 وتنتهي قبل 10.", "solution": "for(int i=0; i<10; i++)"},
    "7": {"title": "📊 7: المصفوفات Arrays", "explanation": "تخزين بيانات من نفس النوع بجانب بعضها.", "example": "int arr[5];", "exercise": "عرف مصفوفة أرقام حجمها 3.", "solution": "int myArr[3];"},
    "8": {"title": "🔤 8: النصوص Strings", "explanation": "التعامل مع النصوص بمكتبة string.", "example": "string s = 'C++';", "exercise": "عرف نصاً قيمته 'Power'.", "solution": "string s = 'Power';"},
    "9": {"title": "⚙️ 9: الدوال Functions", "explanation": "تقسيم البرنامج لأجزاء صغيرة.", "example": "void printHi() { }", "exercise": "عرف دالة لا ترجع شيئاً (void).", "solution": "void func() { }"},
    "10": {"title": "🎯 10: المؤشرات Pointers", "explanation": "متغير يخزن عنوان متغير آخر.", "example": "int* ptr = &x;", "exercise": "عرف مؤشر ptr من نوع int.", "solution": "int* ptr;"},
    "11": {"title": "🔗 11: المراجع References", "explanation": "إعطاء اسم مستعار لمتغير موجود.", "example": "int &ref = x;", "exercise": "عرف مرجعاً للمتغير y.", "solution": "int &ref = y;"},
    "12": {"title": "🧠 12: إدارة الذاكرة", "explanation": "استخدام new لحجز مكان و delete لمسحه.", "example": "int* p = new int;", "exercise": "احجز مساحة لرقم int في الذاكرة.", "solution": "new int;"},
    "13": {"title": "🏗️ 13: الهياكل Structs", "explanation": "تجميع متغيرات مختلفة تحت اسم واحد.", "example": "struct User { int id; };", "exercise": "عرف struct باسم User.", "solution": "struct User { };"},
    "14": {"title": "💎 14: الأصناف Classes", "explanation": "أساس البرمجة كائنية التوجه (OOP).", "example": "class MyClass { };", "exercise": "عرف كلاس باسم Robot.", "solution": "class Robot { };"}
}

# --- معالجات بوت بايثون ---
@bot_py.message_handler(commands=['start'])
def py_start(m):
    mk = types.ReplyKeyboardMarkup(resize_keyboard=True).add("📚 دروس بايثون")
    bot_py.send_message(m.chat.id, "🐍 بوت بايثون التعليمي جاهز!", reply_markup=mk)

@bot_py.message_handler(func=lambda m: m.text == "📚 دروس بايثون")
def py_list(m):
    mk = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    mk.add(*[types.KeyboardButton(f"بايثون {i}") for i in range(1, 13)])
    bot_py.send_message(m.chat.id, "اختر الدرس:", reply_markup=mk)

@bot_py.message_handler(func=lambda m: m.text.startswith("بايثون "))
def py_handler(m):
    num = m.text.split()[1]
    l = lessons_py.get(num)
    if l:
        txt = f"<b>{l['title']}</b>\n\n{l['explanation']}\n\n💻 <b>مثال:</b>\n<code>{l['example']}</code>"
        mk = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("🎯 التحدي", callback_data=f"pyex_{num}"))
        bot_py.send_message(m.chat.id, txt, parse_mode="HTML", reply_markup=mk)

@bot_py.callback_query_handler(func=lambda c: c.data.startswith("py"))
def py_callback(c):
    act, n = c.data.split("_")
    l = lessons_py[n]
    if act == "pyex":
        mk = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("🔑 الحل", callback_data=f"pysol_{n}"))
        bot_py.edit_message_text(f"🎯 <b>التحدي:</b>\n{l['exercise']}", c.message.chat.id, c.message.message_id, parse_mode="HTML", reply_markup=mk)
    else:
        bot_py.edit_message_text(f"✅ <b>الحل:</b>\n<code>{l['solution']}</code>", c.message.chat.id, c.message.message_id, parse_mode="HTML")

# --- معالجات بوت C++ ---
@bot_cpp.message_handler(commands=['start'])
def cpp_start(m):
    mk = types.ReplyKeyboardMarkup(resize_keyboard=True).add("📚 دروس C++")
    bot_cpp.send_message(m.chat.id, "🦾 بوت C++ التعليمي جاهز!", reply_markup=mk)

@bot_cpp.message_handler(func=lambda m: m.text == "📚 دروس C++")
def cpp_list(m):
    mk = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    mk.add(*[types.KeyboardButton(f"C++ {i}") for i in range(1, 15)])
    bot_cpp.send_message(m.chat.id, "اختر درس C++:", reply_markup=mk)

@bot_cpp.message_handler(func=lambda m: m.text.startswith("C++ "))
def cpp_handler(m):
    num = m.text.split()[1]
    l = lessons_cpp.get(num)
    if l:
        txt = f"<b>{l['title']}</b>\n\n{l['explanation']}\n\n💻 <b>مثال:</b>\n<code>{l['example']}</code>"
        mk = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("🎯 التحدي", callback_data=f"cppex_{num}"))
        bot_cpp.send_message(m.chat.id, txt, parse_mode="HTML", reply_markup=mk)

@bot_cpp.callback_query_handler(func=lambda c: c.data.startswith("cpp"))
def cpp_callback(c):
    act, n = c.data.split("_")
    l = lessons_cpp[n]
    if act == "cppex":
        mk = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("🔑 الحل", callback_data=f"cppsol_{n}"))
        bot_cpp.edit_message_text(f"🎯 <b>التحدي:</b>\n{l['exercise']}", c.message.chat.id, c.message.message_id, parse_mode="HTML", reply_markup=mk)
    else:
        bot_cpp.edit_message_text(f"✅ <b>الحل:</b>\n<code>{l['solution']}</code>", c.message.chat.id, c.message.message_id, parse_mode="HTML")

# --- نظام التشغيل الذكي والحماية ---
def run_safe_polling(bot_instance, name):
    while True:
        try:
            print(f"🧹 Clearing {name} Webhook...")
            bot_instance.remove_webhook() # تنظيف تلقائي يغنيك عن الروابط
            print(f"🚀 {name} is Polling...")
            bot_instance.infinity_polling(skip_pending=True, timeout=60)
        except Exception as e:
            print(f"⚠️ {name} Error: {e}. Reconnecting in 10s...")
            time.sleep(10)

def run_health_server():
    class H(http.server.SimpleHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Bot is Alive")
    with socketserver.TCPServer(("", 8000), H) as httpd:
        httpd.serve_forever()

if __name__ == "__main__":
    # تشغيل سيرفر الصحة لـ Koyeb
    threading.Thread(target=run_health_server, daemon=True).start()
    
    # تشغيل بوت بايثون في Thread مستقل
    threading.Thread(target=run_safe_polling, args=(bot_py, "Python Bot"), daemon=True).start()
    
    # تشغيل بوت C++ كالمهمة الأساسية لضمان عدم توقف السيرفر
    print("🌍 All systems active on Koyeb port 8000")
    run_safe_polling(bot_cpp, "C++ Bot")
