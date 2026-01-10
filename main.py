import os
import telebot
import threading
import groq
import time
import html
import streamlit as st
from telebot import types

# --- 🎨 واجهة العرض (لضمان استمرار السيرفر) ---
st.set_page_config(page_title="Bot Empire Console", page_icon="🦾")
st.title("🦾 Bot Empire: Mission Control")
st.success("الإمبراطورية تعمل الآن في السحابة بنجاح!")
st.info("حالة البوتات: متصلة (Online) 🟢")

# --- 🔑 سحب الأسرار من الخزنة ---
TOKEN_PY = os.getenv("TELEGRAM_TOKEN")
TOKEN_CPP = os.getenv("TELEGRAM_TOKEN2")
TOKEN_AI = os.getenv("TELEGRAM_TOKEN3")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# --- 📡 تعريف البوتات ---
bot_py = telebot.TeleBot(TOKEN_PY)
bot_cpp = telebot.TeleBot(TOKEN_CPP)
bot_ai = telebot.TeleBot(TOKEN_AI)
client_llama = groq.Groq(api_key=GROQ_API_KEY)

# --- 🐍 قاعدة بيانات دروس بايثون ---
lessons_py = {
    "1": {"title": "الدرس 1: الطباعة (print) 🐍", "explanation": "دالة print هي أساس عرض النتائج.", "example": "print('مرحباً بك')", "exercise": "اطبع اسمك الثلاثي.", "solution": "print('عثمان ...')"},
    "2": {"title": "الدرس 2: المتغيرات 📦", "explanation": "مخازن لحفظ البيانات.", "example": "name = 'Osman'", "exercise": "عرف متغير x قيمته 10.", "solution": "x = 10"},
    "3": {"title": "الدرس 3: الحساب ➗", "explanation": "العمليات الرياضية الأساسية.", "example": "x = 5 + 5", "exercise": "احسب 10 تقسيم 2.", "solution": "print(10 / 2)"},
    "4": {"title": "الدرس 4: الإدخال 📥", "explanation": "أخذ بيانات من المستخدم.", "example": "input('اسمك؟')", "exercise": "اطلب عمر المستخدم.", "solution": "age = input('كم عمرك؟')"},
    "5": {"title": "الدرس 5: القوائم 📚", "explanation": "تخزين عدة قيم [].", "example": "L = [1, 2, 3]", "exercise": "أنشئ قائمة فواكه.", "solution": "f = ['apple', 'banana']"},
    "6": {"title": "الدرس 6: القواميس 📖", "explanation": "بيانات بنظام (مفتاح: قيمة).", "example": "d = {'a': 1}", "exercise": "أنشئ قاموس لسيارة.", "solution": "car = {'brand': 'Toyota'}"},
    "7": {"title": "الدرس 7: الشروط ⚖️", "explanation": "استخدام if و else.", "example": "if x > 5: print('Ok')", "exercise": "تأكد لو x تساوي 10.", "solution": "if x == 10: print('yes')"},
    "8": {"title": "الدرس 8: التكرار 🔄", "explanation": "حلقة for للتكرار.", "example": "for i in range(5):", "exercise": "اطبع 'Hi' 3 مرات.", "solution": "for i in range(3): print('Hi')"},
    "9": {"title": "الدرس 9: الدوال ⚙️", "explanation": "تجميع الكود في def.", "example": "def my_func():", "exercise": "عرف دالة تطبع 'Go'.", "solution": "def go(): print('Go')"},
    "10": {"title": "الدرس 10: الأخطاء 🛡️", "explanation": "استخدام try و except.", "example": "try: 1/0 \nexcept: print('err')", "exercise": "احمِ كود القسمة من الخطأ.", "solution": "try: print(x/0) \nexcept: pass"},
    "11": {"title": "الدرس 11: الملفات 📂", "explanation": "فتح وقراءة الملفات.", "example": "f = open('file.txt', 'r')", "exercise": "افتح ملف للكتابة.", "solution": "open('test.txt', 'w')"},
    "12": {"title": "الدرس 12: المكتبات 📦", "explanation": "استيراد أكواد جاهزة.", "example": "import math", "exercise": "استورد مكتبة os.", "solution": "import os"}
}

# --- 🦾 قاعدة بيانات دروس C++ ---
lessons_cpp = {
    "1": {"title": "الدرس 1: الهيكل 🏛️", "explanation": "البناء الأساسي لبرنامج C++.", "example": "int main() { return 0; }", "exercise": "اكتب الهيكل.", "solution": "int main() { }"},
    "2": {"title": "الدرس 2: الطباعة 📥", "explanation": "استخدام cout للطباعة.", "example": "cout << 'Hello';", "exercise": "اطبع رقم 100.", "solution": "cout << 100;"},
    "3": {"title": "الدرس 3: الأنواع 📦", "explanation": "تعريف int, double, string.", "example": "int x = 5;", "exercise": "عرف متغير نصي باسم s.", "solution": "string s;"},
    "4": {"title": "الدرس 4: الحساب ➗", "explanation": "العمليات الحسابية في C++.", "example": "int x = 10 / 2;", "exercise": "اضرب 5 في 10.", "solution": "int x = 5 * 10;"},
    "5": {"title": "الدرس 5: الشروط ⚖️", "explanation": "استخدام if و else.", "example": "if (x > 0) { }", "exercise": "تأكد لو x أصغر من 5.", "solution": "if (x < 5) { }"},
    "6": {"title": "الدرس 6: التكرار 🔄", "explanation": "حلقة for في C++.", "example": "for(int i=0; i<5; i++)", "exercise": "كرر 10 مرات.", "solution": "for(int i=0; i<10; i++){ }"},
    "7": {"title": "الدرس 7: المصفوفات 📊", "explanation": "تخزين قيم متتالية.", "example": "int arr[5];", "exercise": "عرف مصفوفة حجمها 10.", "solution": "int a[10];"},
    "8": {"title": "الدرس 8: النصوص 🔤", "explanation": "التعامل مع string.", "example": "string name = 'Ali';", "exercise": "عرف نص باسم msg.", "solution": "string msg;"},
    "9": {"title": "الدرس 9: الدوال ⚙️", "explanation": "تنظيم الكود في functions.", "example": "void fun() { }", "exercise": "عرف دالة باسم start.", "solution": "void start() { }"},
    "10": {"title": "الدرس 10: المؤشرات 🎯", "explanation": "عناوين الذاكرة *.", "example": "int* p = &x;", "exercise": "عرف مؤشر ptr.", "solution": "int* ptr;"},
    "11": {"title": "الدرس 11: المراجع 🔗", "explanation": "اسم مستعار للمتغير &.", "example": "int &ref = x;", "exercise": "عرف مرجع r للمتغير n.", "solution": "int &r = n;"},
    "12": {"title": "الدرس 12: الذاكرة 🧠", "explanation": "حجز ذاكرة ديناميكية new.", "example": "int* p = new int;", "exercise": "احجز ذاكرة لـ float.", "solution": "new float;"},
    "13": {"title": "الدرس 13: Struct 🏗️", "explanation": "تجميع بيانات مختلفة.", "example": "struct User { };", "exercise": "عرف struct باسم Pet.", "solution": "struct Pet { };"},
    "14": {"title": "الدرس 14: Classes 💎", "explanation": "البرمجة الكائنية OOP.", "example": "class Bot { public: };", "exercise": "عرف كلاس باسم AI.", "solution": "class AI { public: };"}
}

# --- 🛠️ وظيفة إرسال الدروس ---
def send_lesson(bot, chat_id, lesson_data, n, prefix):
    try:
        msg = f"<b>{html.escape(lesson_data['title'])}</b>\n\n{html.escape(lesson_data['explanation'])}\n\n💻 <b>مثال:</b>\n<code>{html.escape(lesson_data['example'])}</code>"
        mk = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("🎯 التحدي", callback_data=f"{prefix}_ex_{n}"))
        bot.send_message(chat_id, msg, parse_mode="HTML", reply_markup=mk)
    except Exception as e: print(f"Error: {e}")

# --- 🐍 معالجات بايثون (bot_py) ---
@bot_py.message_handler(commands=['start'])
def py_start(m):
    mk = types.ReplyKeyboardMarkup(resize_keyboard=True).add("🐍 دروس بايثون")
    bot_py.send_message(m.chat.id, "أهلاً بك في Bot Empire بايثون 🐍 يا وحش!", reply_markup=mk)

@bot_py.message_handler(func=lambda m: m.text == "🐍 دروس بايثون")
def py_list(m):
    mk = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    btns = [types.KeyboardButton(f"بايثون {i}") for i in range(1, 13)]
    mk.add(*btns)
    bot_py.send_message(m.chat.id, "اختر الدرس يا بطل:", reply_markup=mk)

@bot_py.message_handler(func=lambda m: m.text and m.text.startswith("بايثون "))
def py_h(m):
    n = m.text.split()[1]
    if n in lessons_py: send_lesson(bot_py, m.chat.id, lessons_py[n], n, "py")

@bot_py.callback_query_handler(func=lambda c: c.data.startswith("py_"))
def py_c(c):
    _, act, n = c.data.split("_")
    if act == "ex":
        mk = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("🔑 الحل", callback_data=f"py_sol_{n}"))
        bot_py.edit_message_text(f"🎯 التحدي: {lessons_py[n]['exercise']}", c.message.chat.id, c.message.message_id, reply_markup=mk)
    elif act == "sol":
        bot_py.edit_message_text(f"✅ الحل: <code>{lessons_py[n]['solution']}</code>", c.message.chat.id, c.message.message_id, parse_mode="HTML")

# --- 🦾 معالجات C++ (bot_cpp) ---
@bot_cpp.message_handler(commands=['start'])
def cpp_start(m):
    mk = types.ReplyKeyboardMarkup(resize_keyboard=True).add("🦾 دروس C++")
    bot_cpp.send_message(m.chat.id, "أهلاً بك في Bot Empire C++ 🦾 يا بطل!", reply_markup=mk)

@bot_cpp.message_handler(func=lambda m: m.text == "🦾 دروس C++")
def cpp_list(m):
    mk = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    btns = [types.KeyboardButton(f"الدرس {i}") for i in range(1, 15)]
    mk.add(*btns)
    bot_cpp.send_message(m.chat.id, "اختر الدرس يا وحش:", reply_markup=mk)

@bot_cpp.message_handler(func=lambda m: m.text and m.text.startswith("الدرس "))
def cpp_h(m):
    n = m.text.split()[1]
    if n in lessons_cpp: send_lesson(bot_cpp, m.chat.id, lessons_cpp[n], n, "cp")

@bot_cpp.callback_query_handler(func=lambda c: c.data.startswith("cp_"))
def cpp_c(c):
    _, act, n = c.data.split("_")
    if act == "ex":
        mk = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("🔑 الحل", callback_data=f"cp_sol_{n}"))
        bot_cpp.edit_message_text(f"🎯 التحدي: {lessons_cpp[n]['exercise']}", c.message.chat.id, c.message.message_id, reply_markup=mk)
    elif act == "sol":
        bot_cpp.edit_message_text(f"✅ الحل: <code>{lessons_cpp[n]['solution']}</code>", c.message.chat.id, c.message.message_id, parse_mode="HTML")

# --- 🤖 معالج الذكاء الاصطناعي (bot_ai) ---
@bot_ai.message_handler(func=lambda m: True)
def ai_handler(m):
    try:
        resp = client_llama.chat.completions.create(
            messages=[
                {"role": "system", "content": "أنت 'مستشار Bot Empire التقني'؛ خبير تقني وفلسفي. علم المستخدم البرمجة والأمن السيبراني بلهجة سعودية وناده بـ يا بطل."},
                {"role": "user", "content": m.text}
            ],
            model="llama-3.1-8b-instant",
        )
        bot_ai.reply_to(m, resp.choices[0].message.content)
    except: bot_ai.reply_to(m, "يا بطل، السيرفر عليه ضغط، جرب مرة ثانية.")

# --- 🚀 محرك التشغيل الجبار (استبدل الجزء الأخير بهذا) ---

def run_bot_wrapper(bot, name):
    while True:
        try:
            bot.remove_webhook() # تنظيف أي اتصال معلق
            print(f"📡 {name} is now polling...")
            bot.polling(none_stop=True, interval=1, timeout=60)
        except Exception as e:
            print(f"⚠️ {name} Error: {e}")
            time.sleep(5)

# تشغيل البوتات وضمان عدم تكرارها
if "empire_online" not in st.session_state:
    threading.Thread(target=run_bot_wrapper, args=(bot_py, "Python Bot"), daemon=True).start()
    threading.Thread(target=run_bot_wrapper, args=(bot_cpp, "C++ Bot"), daemon=True).start()
    threading.Thread(target=run_bot_wrapper, args=(bot_ai, "AI Bot"), daemon=True).start()
    st.session_state.empire_online = True

st.write("---")
st.success("🤖 **إمبراطورية البوتات مفعّلة الآن!**")
st.write("جميع البوتات (بايثون، C++، والذكاء الاصطناعي) تعمل في الخلفية.")
