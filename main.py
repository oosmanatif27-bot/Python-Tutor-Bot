import os
import telebot
import threading
import http.server
import socketserver
import groq # تأكد من وجود هذا السطر فوق مع الـ imports
import time
import html
from telebot import types

# --- 🔑 إعدادات المفاتيح ---
TOKEN_PY = os.getenv("TELEGRAM_TOKEN")
TOKEN_CPP = os.getenv("TELEGRAM_TOKEN2")
TOKEN_GEMINI = os.getenv("TELEGRAM_TOKEN3")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# --- 📡 تعريف البوتات ---
bot_py = telebot.TeleBot(TOKEN_PY)
bot_cpp = telebot.TeleBot(TOKEN_CPP)
bot_gemini = telebot.TeleBot(TOKEN_GEMINI)

# [ملاحظة: دروس بايثون و C++ تبقى كما هي في كودك لضمان عدم ضياع البيانات]

# --- 🐍 دروس بايثون (نفس الدروس اللي عندك) ---
lessons_py = {
    "1": {"title": "الدرس 1: الطباعة (print) 🐍", "explanation": "دالة printو هي أول خطوة لتعلم أي لغة برمجة، ووظيفتها عرض النصوص والنتائج .", "example": "print('مرحباً بك')", "exercise": "اطبع اسمك الثلاثي.", "solution": "print('عثمان ...')"},
    "2": {"title": "الدرس 2: المتغيرات 📦", "explanation": "المتغيرات هي مخازن في الذاكرة نحفظ فيها البيانات.", "example": "name = 'Osman'\nage = 20", "exercise": "عرف متغير باسم country وضع فيه اسم بلدك.", "solution": "country = 'Saudi Arabia'"},
    "3": {"title": "الدرس 3: الحساب ➗", "explanation": "بايثون بارعة في الحساب (+, -, *, /).", "example": "x = 10 + 5", "exercise": "احسب حاصل ضرب 5 في 5.", "solution": "print(5 * 5)"},
    "4": {"title": "الدرس 4: الإدخال (input) 📥", "explanation": "دالة input تأخذ معلومات من المستخدم.", "example": "name = input('ما اسمك؟')", "exercise": "اطلب عمر المستخدم.", "solution": "age = input('كم عمرك؟')"},
    "5": {"title": "الدرس 5: القوائم (Lists) 📚", "explanation": "تخزين قيم كثيرة في متغير واحد [].", "example": "items = [1, 2, 3]", "exercise": "أنشئ قائمة فيها 3 ألوان.", "solution": "colors = ['Red', 'Blue', 'Green']"},
    "6": {"title": "الدرس 6: القواميس 📖", "explanation": "تخزين البيانات بنظام مفتاح وقيمة {}.", "example": "d = {'id': 1}", "exercise": "أنشئ قاموس فيه 'city': 'Riyadh'.", "solution": "d = {'city': 'Riyadh'}"},
    "7": {"title": "الدرس 7: الشروط (if) ⚖️", "explanation": "لاتخاذ القرارات في الكود.", "example": "if x > 0: print('ok')", "exercise": "اطبع 'ناجح' إذا كانت الدرجة s أكبر من 50.", "solution": "if s > 50: print('ناجح')"},
    "8": {"title": "الدرس 8: التكرار (for) 🔄", "explanation": "لتكرار الكود عدة مرات.", "example": "for i in range(3): print(i)", "exercise": "اطبع كلمة 'Hello' 5 مرات.", "solution": "for i in range(5): print('Hello')"},
    "9": {"title": "الدرس 9: الدوال (Functions) ⚙️", "explanation": "كتلة كود نستخدمها متى ما بغينا.", "example": "def hi(): print('hi')", "exercise": "عرف دالة باسم go تطبع 'Go'.", "solution": "def go(): print('Go')"},
    "10": {"title": "الدرس 10: الأخطاء (try) 🛡️", "explanation": "لحماية البرنامج من الانهيار.", "example": "try: 1/0 \nexcept: print('error')", "exercise": "استخدم try لتجنب خطأ القسمة.", "solution": "try: x=1/0 \nexcept: pass"},
    "11": {"title": "الدرس 11: الملفات 📂", "explanation": "القراءة والكتابة على الملفات.", "example": "open('f.txt', 'w')", "exercise": "افتح ملف test.txt للقراءة.", "solution": "open('test.txt', 'r')"},
    "12": {"title": "الدرس 12: المكتبات 📦", "explanation": "استخدام أكواد جاهزة.", "example": "import math", "exercise": "استورد مكتبة time.", "solution": "import time"}
}

# --- 🦾 دروس C++ (نفس الدروس اللي عندك) ---
lessons_cpp = {
    "1": {"title": "الدرس 1: الهيكل 🏛️", "explanation": "أساس كل برنامج C++.", "example": "int main() { return 0; }", "exercise": "اكتب الهيكل.", "solution": "int main() { }"},
    "2": {"title": "الدرس 2: الطباعة 📥", "explanation": "استخدام cout.", "example": "cout << 'Hi';", "exercise": "اطبع 'Bot'.", "solution": "cout << 'Bot';"},
    "3": {"title": "الدرس 3: الأنواع 📦", "explanation": "int, double, string.", "example": "int x = 5;", "exercise": "عرف x كـ double.", "solution": "double x;"},
    "4": {"title": "الدرس 4: الحساب ➗", "explanation": "العمليات الرياضية.", "example": "x = 10 / 2;", "exercise": "اضرب 2 في 4.", "solution": "int x = 2 * 4;"},
    "5": {"title": "الدرس 5: الشروط ⚖️", "explanation": "استخدام if و else.", "example": "if(x==1){}", "exercise": "تأكد لو x أكبر من 10.", "solution": "if(x > 10){ }"},
    "6": {"title": "الدرس 6: التكرار 🔄", "explanation": "حلقة for.", "example": "for(int i=0;i<5;i++){}", "exercise": "كرر 10 مرات.", "solution": "for(int i=0;i<10;i++){ }"},
    "7": {"title": "الدرس 7: المصفوفات 📊", "explanation": "تخزين مصفوفة أرقام.", "example": "int a[5];", "exercise": "عرف مصفوفة حجمها 3.", "solution": "int a[3];"},
    "8": {"title": "الدرس 8: النصوص 🔤", "explanation": "استخدام string.", "example": "string s = 'hi';", "exercise": "عرف نص باسم msg.", "solution": "string msg;"},
    "9": {"title": "الدرس 9: الدوال ⚙️", "explanation": "تنظيم الكود.", "example": "void f(){}", "exercise": "عرف دالة باسم run.", "solution": "void run(){ }"},
    "10": {"title": "الدرس 10: المؤشرات 🎯", "explanation": "عناوين الذاكرة.", "example": "int* p = &x;", "exercise": "عرف مؤشر ptr.", "solution": "int* ptr;"},
    "11": {"title": "الدرس 11: المراجع 🔗", "explanation": "اسم مستعار للمتغير.", "example": "int &r = x;", "exercise": "عرف مرجع r للمتغير n.", "solution": "int &r = n;"},
    "12": {"title": "الدرس 12: الذاكرة 🧠", "explanation": "استخدام new.", "example": "int* p = new int;", "exercise": "احجز ذاكرة لـ double.", "solution": "new double;"},
    "13": {"title": "الدرس 13: Struct 🏗️", "explanation": "بيانات مخصصة.", "example": "struct S {};", "exercise": "عرف struct باسم Car.", "solution": "struct Car {};"},
    "14": {"title": "الدرس 14: Classes 💎", "explanation": "أساس الـ OOP.", "example": "class C { public: };", "exercise": "عرف كلاس Robot.", "solution": "class Robot { public: };"}
}

# --- 🛠️ وظائف الدروس (تم تحسينها بـ try) ---
def send_lesson(bot, chat_id, lesson_data, n, prefix):
    try:
        safe_title = html.escape(lesson_data['title'])
        safe_expl = html.escape(lesson_data['explanation'])
        safe_exam = html.escape(lesson_data['example'])
        msg_text = f"<b>{safe_title}</b>\n\n{safe_expl}\n\n💻 <b>مثال:</b>\n<code>{safe_exam}</code>"
        mk = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("🎯 التحدي", callback_data=f"{prefix}_ex_{n}"))
        bot.send_message(chat_id, msg_text, parse_mode="HTML", reply_markup=mk)
    except Exception as e:
        print(f"Error sending lesson: {e}")

# --- 🐍 معالجات بايثون ---
@bot_py.message_handler(commands=['start'])
def py_start(m):
    mk = types.ReplyKeyboardMarkup(resize_keyboard=True).add("🐍 دروس بايثون")
    bot_py.send_message(m.chat.id, f"أهلاً بك في Bot Empire بايثون 🐍 يا وحش!", reply_markup=mk)

@bot_py.message_handler(func=lambda m: m.text == "🐍 دروس بايثون")
def py_list(m):
    mk = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    btns = [types.KeyboardButton(f"بايثون {i}") for i in range(1, 13)]
    mk.add(*btns)
    bot_py.send_message(m.chat.id, "اختر الدرس يا بطل:", reply_markup=mk)

@bot_py.message_handler(func=lambda m: m.text and m.text.startswith("بايثون "))
def py_handler(m):
    try:
        n = m.text.split()[1]
        if n in lessons_py: send_lesson(bot_py, m.chat.id, lessons_py[n], n, "py")
    except: pass

@bot_py.callback_query_handler(func=lambda c: c.data.startswith("py_"))
def py_callback(c):
    try:
        act, n = c.data.split("_")[1], c.data.split("_")[2]
        if act == "ex":
            mk = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("🔑 الحل", callback_data=f"py_sol_{n}"))
            bot_py.edit_message_text(f"🎯 التحدي: {lessons_py[n]['exercise']}", c.message.chat.id, c.message.message_id, reply_markup=mk)
        elif act == "sol":
            bot_py.edit_message_text(f"✅ الحل: <code>{lessons_py[n]['solution']}</code>", c.message.chat.id, c.message.message_id, parse_mode="HTML")
    except: pass

# --- 🦾 معالجات C++ ---
@bot_cpp.message_handler(commands=['start'])
def cpp_start(m):
    mk = types.ReplyKeyboardMarkup(resize_keyboard=True).add("🦾 دروس C++")
    bot_cpp.send_message(m.chat.id, f"أهلاً بك في Bot Empire C++ 🦾 يا بطل!", reply_markup=mk)

@bot_cpp.message_handler(func=lambda m: m.text == "🦾 دروس C++")
def cpp_list(m):
    mk = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    btns = [types.KeyboardButton(f"الدرس {i}") for i in range(1, 15)]
    mk.add(*btns)
    bot_cpp.send_message(m.chat.id, "اختر الدرس يا وحش:", reply_markup=mk)

@bot_cpp.message_handler(func=lambda m: m.text and m.text.startswith("الدرس "))
def cpp_handler(m):
    try:
        n = m.text.split()[1]
        if n in lessons_cpp: send_lesson(bot_cpp, m.chat.id, lessons_cpp[n], n, "cp")
    except: pass

@bot_cpp.callback_query_handler(func=lambda c: c.data.startswith("cp_"))
def cpp_callback(c):
    try:
        act, n = c.data.split("_")[1], c.data.split("_")[2]
        if act == "ex":
            mk = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("🔑 الحل", callback_data=f"cp_sol_{n}"))
            bot_cpp.edit_message_text(f"🎯 التحدي: {lessons_cpp[n]['exercise']}", c.message.chat.id, c.message.message_id, reply_markup=mk)
        elif act == "sol":
            bot_cpp.edit_message_text(f"✅ الحل: <code>{lessons_cpp[n]['solution']}</code>", c.message.chat.id, c.message.message_id, parse_mode="HTML")
    except: pass

# --- 🤖 إعداد Llama 3 (البوت الثالث) ---
# حط المفتاح اللي جبته من موقع Groq في الـ Environment Variables باسم GROQ_API_KEY
client_llama = groq.Groq(api_key=os.getenv("GROQ_API_KEY"))

@bot_gemini.message_handler(func=lambda m: True)
def ai_bot_handler(m):
    try:
        # إرسال السؤال لـ Llama 3
        response = client_llama.chat.completions.create(
            messages=[
                {"role": "system", "content":"أنت 'مستشار Bot Empire التقني'؛ خبير عاقل ورصين. مهمتك تعليم المستخدمين البرمجة والأمن السيبراني بأسلوب فلسفي وعميق. استخدم اللهجة السعودية البيضاء ونادِ المستخدم بـ يا بطل."},
                {"role": "user", "content": m.text}
            ],
            #model="llama3-8b-8192", # الموديل السريع والجبار
            model="llama-3.1-8b-instant", #ممكن يشتغل
        )
        
        # الرد على المستخدم
        bot_gemini.reply_to(m, response.choices[0].message.content)
        
    except Exception as e:
        print(f"❌ Llama Error: {e}")
        bot_gemini.reply_to(m, "يا وحش حصل ضغط على السيرفر، جرب ترسل رسالتك مرة ثانية.")

# --- 🚀 تشغيل النظام (نسخة CAN المستقرة) ---
def run_bot(bot, name):
    print(f"📡 {name} is starting...")
    while True:
        try:
            # استخدام polling العادي داخل loop لضمان إعادة التشغيل عند الخطأ
            bot.polling(none_stop=True, interval=1, timeout=30)
        except Exception as e:
            print(f"⚠️ {name} disconnected: {e}. Reconnecting in 5s...")
            time.sleep(5)

if __name__ == "__main__":
    # تشغيل سيرفر الويب (Health Check)
    PORT = int(os.getenv("PORT", 8000))
    def start_server():
        with socketserver.TCPServer(("", PORT), http.server.SimpleHTTPRequestHandler) as httpd:
            httpd.serve_forever()
    
    threading.Thread(target=start_server, daemon=True).start()
    
    threads = [
        threading.Thread(target=run_bot, args=(bot_py, "Python Bot")),
        threading.Thread(target=run_bot, args=(bot_cpp, "C++ Bot")),
        threading.Thread(target=run_bot, args=(bot_gemini, "Gemini Bot"))
    ]
    for t in threads: t.start()
    print("🚀 Bot Empire is fully active and protected by CAN!")
    for t in threads: t.join()






