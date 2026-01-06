import os, telebot, threading, http.server, socketserver, time
from telebot import types

# جلب التوكن من إعدادات كويب
TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = telebot.TeleBot(TOKEN)

# --- المنهج العلمي المبسط (12 درس كاملة) ---
lessons_data = {
    "1": {"title": "الدرس 1: دالة print", "explanation": "دالة الإخراج للنصوص (String) والأرقام (Integer).", "example": "print('عثمان', 1)", "exercise": "اطبع اسمك ورقم 5.", "solution": "print('عثمان', 5)"},
    "2": {"title": "الدرس 2: Variables", "explanation": "تخزين البيانات في الذاكرة باسم معين.", "example": "x = 10", "exercise": "خزن نص 'بايثون' في متغير a.", "solution": "a = 'بايثون'"},
    "3": {"title": "الدرس 3: Math", "explanation": "العمليات الحسابية الأساسية (+, -, *, /).", "example": "print(5 + 5)", "exercise": "اجمع 100 و 200.", "solution": "print(100 + 200)"},
    "4": {"title": "الدرس 4: Input", "explanation": "استقبال البيانات من المستخدم (تكون نصاً دائماً).", "example": "name = input('اسمك؟')", "exercise": "اسأل المستخدم عن بلده.", "solution": "country = input('بلدك؟')"},
    "5": {"title": "الدرس 5: Lists", "explanation": "مجموعة عناصر مرتبة تبدأ من الفهرس 0.", "example": "L = [1, 2, 3]", "exercise": "اصنع قائمة فيها 'أ' و 'ب'.", "solution": "L = ['أ', 'ب']"},
    "6": {"title": "الدرس 6: Dictionaries", "explanation": "بيانات بنظام مفتاح وقيمة Key-Value.", "example": "d = {'id': 1}", "exercise": "اصنع قاموساً فيه اسمك وعمرك.", "solution": "d = {'name': 'عثمان', 'age': 20}"},
    "7": {"title": "الدرس 7: If Statements", "explanation": "اتخاذ القرارات البرمجية بناءً على شرط.", "example": "if x > 0: print('موجب')", "exercise": "اكتب شرطاً لو y يساوي 10.", "solution": "if y == 10: print('صح')"},
    "8": {"title": "الدرس 8: Loops", "explanation": "تكرار الكود آلياً لعدد محدد من المرات.", "example": "for i in range(3): print(i)", "exercise": "كرر طباعة 'تم' 5 مرات.", "solution": "for i in range(5): print('تم')"},
    "9": {"title": "الدرس 9: Functions", "explanation": "أكواد قابلة لإعادة الاستخدام تبدأ بـ def.", "example": "def my_func(): pass", "exercise": "عرف دالة باسم start.", "solution": "def start(): print('بدأنا')"},
    "10": {"title": "الدرس 10: Errors", "explanation": "استخدام try و except لمنع انهيار البرنامج.", "example": "try: 1/0 except: pass", "exercise": "جرب كوداً داخل try.", "solution": "try: print(x) except: print('خطأ')"},
    "11": {"title": "الدرس 11: Files", "explanation": "التعامل مع الملفات الخارجية (قراءة وكتابة).", "example": "open('test.txt', 'r')", "exercise": "افتح ملفاً للكتابة باسم a.txt.", "solution": "f = open('a.txt', 'w')"},
    "12": {"title": "الدرس 12: Modules", "explanation": "استيراد مكتبات وأدوات مبرمجة مسبقاً.", "example": "import math", "exercise": "استورد مكتبة الوقت time.", "solution": "import time"}
}

# --- إدارة الرسائل والقوائم ---

@bot.message_handler(commands=['start'])
def welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add("مقدمة بايثون", "قائمة الدروس")
    bot.send_message(message.chat.id, "🚀 أهلاً بك! أنا مدرب بايثون الخاص بك.\nاختر 'قائمة الدروس' لتبدأ:", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text == "مقدمة بايثون")
def intro(message):
    text = "بايثون لغة برمجة قوية وسهلة، تُستخدم في صنع الألعاب والذكاء الاصطناعي."
    bot.send_message(message.chat.id, text)

@bot.message_handler(func=lambda m: m.text == "قائمة الدروس")
def list_lessons(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    # توليد الأزرار لجميع الدروس الـ 12
    btns = [types.KeyboardButton(f"الدرس {i}") for i in range(1, 13)]
    markup.add(*btns, "الرجوع للقائمة الرئيسية")
    bot.send_message(message.chat.id, "📚 اختر الدرس الذي تريد تعلمه:", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text and m.text.startswith("الدرس "))
def open_lesson(message):
    # استخراج الرقم فقط من النص (مثل 'الدرس 4' -> '4')
    num = "".join(filter(str.isdigit, message.text))
    if num in lessons_data:
        l = lessons_data[num]
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🎯 ابدأ التحدي", callback_data=f"ex_{num}"))
        bot.send_message(message.chat.id, f"💡 *{l['title']}*\n\n{l['explanation']}\n\n*مثال:*\n`{l['example']}`", reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    l_id = call.data.split("_")[1]
    l = lessons_data[l_id]
    if call.data.startswith("ex_"):
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🔑 كشف الحل", callback_data=f"sol_{l_id}"))
        bot.edit_message_text(f"🎯 *التحدي:*\n{l['exercise']}", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
    elif call.data.startswith("sol_"):
        bot.edit_message_text(f"✅ *الحل العلمي:*\n`{l['solution']}`\n\nأحسنت يا بطل! 🚀", call.message.chat.id, call.message.message_id, parse_mode="Markdown")

# --- نظام الحماية والتشغيل ---

def run_health():
    try: socketserver.TCPServer(("", 8000), http.server.SimpleHTTPRequestHandler).serve_forever()
    except: pass

if __name__ == "__main__":
    threading.Thread(target=run_health, daemon=True).start()
    
    # حل مشكلة الـ Conflict بتنظيف الجلسة والانتظار
    try:
        bot.remove_webhook()
        time.sleep(2) 
        print("✅ البوت يعمل الآن بنجاح!")
        bot.infinity_polling(skip_pending=True)
    except Exception as e:
        print(f"❌ خطأ: {e}")
