import os, telebot, threading, http.server, socketserver, time
from telebot import types

# --- إعدادات التوكنات ---
TOKEN_PY = os.getenv("TELEGRAM_TOKEN")   # توكن بوت بايثون
TOKEN_CPP = os.getenv("TELEGRAM_TOKEN2") # توكن بوت C++

bot_py = telebot.TeleBot(TOKEN_PY)
bot_cpp = telebot.TeleBot(TOKEN_CPP)

user_warnings_cpp = {} # عداد لبوت C++

# --- قاعدة بيانات دروس بايثون (12 درس) ---
lessons_py = {
    "1": {"title": "الدرس 1: دالة print 💡", "explanation": "عرض النتائج.", "example": "print('Hi')", "exercise": "اطبع Python", "solution": "print('Python')"},
    "2": {"title": "الدرس 2: المتغيرات 💡", "explanation": "تخزين البيانات.", "example": "x = 5", "exercise": "عرف x بـ 10", "solution": "x = 10"},
    "3": {"title": "الدرس 3: الحساب 💡", "explanation": "الجمع والطرح.", "example": "1+1", "exercise": "اضرب 2 في 3", "solution": "print(2*3)"},
    "4": {"title": "الدرس 4: المدخلات 💡", "explanation": "سؤال المستخدم.", "example": "input()", "exercise": "اطلب العمر", "solution": "age = input()"},
    "5": {"title": "الدرس 5: القوائم 💡", "explanation": "صندوق بيانات.", "example": "[1,2]", "exercise": "أنشئ قائمة", "solution": "L = [1]"},
    "6": {"title": "الدرس 6: القواميس 💡", "explanation": "مفتاح وقيمة.", "example": "{'a':1}", "exercise": "أنشئ قاموس", "solution": "d = {'id':1}"},
    "7": {"title": "الدرس 7: الشروط 💡", "explanation": "اتخاذ قرار.", "example": "if x > 0:", "exercise": "شرط x يساوي 5", "solution": "if x == 5:"},
    "8": {"title": "الدرس 8: التكرار 💡", "explanation": "تنفيذ مكرر.", "example": "for i in range(5):", "exercise": "كرر 3 مرات", "solution": "for i in range(3):"},
    "9": {"title": "الدرس 9: الدوال 💡", "explanation": "تجميع الكود.", "example": "def f():", "exercise": "عرف دالة", "solution": "def start():"},
    "10": {"title": "الدرس 10: الأخطاء 💡", "explanation": "منع الانهيار.", "example": "try:", "exercise": "استخدم try", "solution": "try: pass"},
    "11": {"title": "الدرس 11: الملفات 💡", "explanation": "قراءة ملف.", "example": "open('f.txt')", "exercise": "افتح ملف", "solution": "open('d.txt')"},
    "12": {"title": "الدرس 12: المكتبات 💡", "explanation": "أدوات جاهزة.", "example": "import math", "exercise": "استورد time", "solution": "import time"}
}

# --- قاعدة بيانات دروس C++ (14 درس) ---
lessons_cpp = {
    "1": {"title": "🏛️ 1: هيكل البرنامج", "explanation": "المكتبات ودالة main.", "example": "int main() { }", "exercise": "اكتب الهيكل", "solution": "int main() { return 0; }"},
    "2": {"title": "📥 2: الطباعة والإدخال", "explanation": "cout و cin.", "example": "cin >> x;", "exercise": "استقبل رقم", "solution": "cin >> num;"},
    "3": {"title": "📦 3: أنواع البيانات", "explanation": "int, char, bool.", "example": "bool ok = true;", "exercise": "عرف bool", "solution": "bool x = true;"},
    "4": {"title": "➗ 4: العمليات الحسابية", "explanation": "الجمع وباقي القسمة %.", "example": "10 % 3", "exercise": "احسب باقي 5/2", "solution": "5 % 2"},
    "5": {"title": "⚖️ 5: الجمل الشرطية", "explanation": "if, else, switch.", "example": "switch(x) { }", "exercise": "شرط x اكبر من 0", "solution": "if(x>0){}"},
    "6": {"title": "🔄 6: الحلقات التكرارية", "explanation": "for, while.", "example": "for(int i=0; i<5; i++)", "exercise": "حلقة تكرار 10", "solution": "for(int i=0; i<10; i++)"},
    "7": {"title": "📊 7: المصفوفات", "explanation": "تخزين متسلسل.", "example": "int arr[5];", "exercise": "عرف مصفوفة 3", "solution": "int a[3];"},
    "8": {"title": "🔤 8: النصوص", "explanation": "مكتبة string.", "example": "string s = 'Hi';", "exercise": "عرف نص", "solution": "string s;"},
    "9": {"title": "⚙️ 9: الدوال", "explanation": "تنظيم الكود.", "example": "void f() { }", "exercise": "عرف دالة void", "solution": "void run() { }"},
    "10": {"title": "🎯 10: المؤشرات (Pointers)", "explanation": "عناوين الذاكرة (هام للأمن).", "example": "int* p = &x;", "exercise": "عرف مؤشر ptr", "solution": "int* ptr;"},
    "11": {"title": "🔗 11: المراجع", "explanation": "اسم مستعار للمتغير.", "example": "int &r = x;", "exercise": "عرف مرجع", "solution": "int &ref = y;"},
    "12": {"title": "🧠 12: إدارة الذاكرة", "explanation": "new و delete.", "example": "int* p = new int;", "exercise": "احجز ذاكرة", "solution": "new int;"},
    "13": {"title": "🏗️ 13: الهياكل (Structs)", "explanation": "تجميع بيانات.", "example": "struct D { };", "exercise": "عرف struct", "solution": "struct S { };"},
    "14": {"title": "💎 14: الأصناف (OOP)", "explanation": "الكلاسات والكائنات.", "example": "class C { };", "exercise": "عرف كلاس", "solution": "class A { };"}
}

# --- منطق بوت البايثون ---
@bot_py.message_handler(commands=['start'])
def py_start(m):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True).add("قائمة الدروس")
    bot_py.send_message(m.chat.id, "🚀 بوت تعليم بايثون جاهز!", reply_markup=markup)

@bot_py.message_handler(func=lambda m: m.text == "قائمة الدروس")
def py_list(m):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    markup.add(*[types.KeyboardButton(f"الدرس {i}") for i in range(1, 13)])
    bot_py.send_message(m.chat.id, "📚 اختر درس بايثون:", reply_markup=markup)

@bot_py.message_handler(func=lambda m: m.text.startswith("الدرس "))
def py_h(m):
    num = "".join(filter(str.isdigit, m.text))
    l = lessons_py.get(num)
    if l:
        txt = f"<b>{l['title']}</b>\n\n{l['explanation']}\n\n<code>{l['example']}</code>"
        mk = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("🎯 التحدي", callback_data=f"pyex_{num}"))
        bot_py.send_message(m.chat.id, txt, parse_mode="HTML", reply_markup=mk)

# --- منطق بوت C++ ---
@bot_cpp.message_handler(commands=['start'])
def cpp_start(m):
    user_warnings_cpp[m.chat.id] = 0
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True).add("📚 قائمة دروس C++")
    bot_cpp.send_message(m.chat.id, "👋 مرحباً بك في دورة C++!", reply_markup=markup)

@bot_cpp.message_handler(func=lambda m: m.text == "📚 قائمة دروس C++")
def cpp_list(m):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    markup.add(*[types.KeyboardButton(f"الدرس {i}") for i in range(1, 15)])
    bot_cpp.send_message(m.chat.id, "اختر درس C++:", reply_markup=markup)

@bot_cpp.message_handler(func=lambda m: m.text.startswith("الدرس "))
def cpp_h(m):
    num = "".join(filter(str.isdigit, m.text))
    l = lessons_cpp.get(num)
    if l:
        txt = f"<b>{l['title']}</b>\n\n{l['explanation']}\n\n<code>{l['example']}</code>"
        mk = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("🎯 التحدي", callback_data=f"cppex_{num}"))
        bot_cpp.send_message(m.chat.id, txt, parse_mode="HTML", reply_markup=mk)

# --- معالج الأزرار (Inline) للكل ---
@bot_py.callback_query_handler(func=lambda c: c.data.startswith("py"))
def py_callback(c):
    act, n = c.data.split("_")
    l = lessons_py.get(n)
    if act == "pyex":
        mk = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("🔑 الحل", callback_data=f"pysol_{n}"))
        bot_py.edit_message_text(f"🎯 التحدي:\n{l['exercise']}", c.message.chat.id, c.message.message_id, reply_markup=mk)
    else: bot_py.edit_message_text(f"✅ الحل:\n<code>{l['solution']}</code>", c.message.chat.id, c.message.message_id, parse_mode="HTML")

@bot_cpp.callback_query_handler(func=lambda c: c.data.startswith("cpp"))
def cpp_callback(c):
    act, n = c.data.split("_")
    l = lessons_cpp.get(n)
    if act == "cppex":
        mk = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("🔑 الحل", callback_data=f"cppsol_{n}"))
        bot_cpp.edit_message_text(f"🎯 التحدي:\n{l['exercise']}", c.message.chat.id, c.message.message_id, reply_markup=mk)
    else: bot_cpp.edit_message_text(f"✅ الحل:\n<code>{l['solution']}</code>", c.message.chat.id, c.message.message_id, parse_mode="HTML")

# --- نظام الحماية والتشغيل ---
def run_health():
    class H(http.server.SimpleHTTPRequestHandler):
        def do_GET(self): self.send_response(200); self.end_headers(); self.wfile.write(b"OK")
    with socketserver.TCPServer(("", 8000), H) as httpd: httpd.serve_forever()

if __name__ == "__main__":
    threading.Thread(target=run_health, daemon=True).start() # تشغيل سيرفر الإنقاذ
    threading.Thread(target=lambda: bot_py.infinity_polling(skip_pending=True), daemon=True).start() # بوت بايثون
    print("🚀 Both Bots are Running on Koyeb!")
    bot_cpp.infinity_polling(skip_pending=True) # بوت C++
