import os, telebot, threading, http.server, socketserver, time
from telebot import types

# جلب التوكن من متغيرات البيئة
TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = telebot.TeleBot(TOKEN)

# بيانات الدروس - تم استخدام .get() للحماية من الأخطاء
lessons_data = {
    "1": {"title": "الدرس 1: print", "explanation": "عرض النصوص.", "example": "print('Hi')", "exercise": "اطبع اسمك.", "solution": "print('Osman')"},
    "2": {"title": "الدرس 2: Variables", "explanation": "المتغيرات.", "example": "x = 5", "exercise": "عرف x.", "solution": "x = 5"},
    "3": {"title": "الدرس 3: Math", "explanation": "الحساب.", "example": "1+1", "exercise": "اجمع 2+2.", "solution": "2+2"},
    "4": {"title": "الدرس 4: Input", "explanation": "المدخلات.", "example": "input()", "exercise": "اسأل عن الاسم.", "solution": "input('name')"},
    "5": {"title": "الدرس 5: Lists", "explanation": "القوائم.", "example": "[]", "exercise": "اصنع قائمة.", "solution": "l = []"},
    "6": {"title": "الدرس 6: Dictionaries", "explanation": "القواميس.", "example": "{}", "exercise": "اصنع قاموس.", "solution": "d = {}"},
    "7": {"title": "الدرس 7: If", "explanation": "الشروط.", "example": "if x:", "exercise": "ضع شرط.", "solution": "if x == 1:"},
    "8": {"title": "الدرس 8: Loops", "explanation": "التكرار.", "example": "for i:", "exercise": "كرر 3 مرات.", "solution": "for i in range(3):"},
    "9": {"title": "الدرس 9: Functions", "explanation": "الدوال.", "example": "def f():", "exercise": "عرف دالة.", "solution": "def hi():"},
    "10": {"title": "الدرس 10: Errors", "explanation": "الأخطاء.", "example": "try:", "exercise": "استخدم try.", "solution": "try: pass"},
    "11": {"title": "الدرس 11: Files", "explanation": "الملفات.", "example": "open()", "exercise": "افتح ملف.", "solution": "open('a.txt')"},
    "12": {"title": "الدرس 12: Modules", "explanation": "المكتبات.", "example": "import", "exercise": "استورد math.", "solution": "import math"}
}

@bot.message_handler(commands=['start'])
def welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("قائمة الدروس")
    bot.send_message(message.chat.id, "🚀 البوت يعمل الآن! اختر من القائمة:", reply_markup=markup)

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
        title = l.get('title', 'N/A')
        expl = l.get('explanation', 'N/A')
        exmp = l.get('example', 'N/A')
        
        text = f"💡 *{title}*\n\n📖 {expl}\n\n💻 *مثال:*\n`{exmp}`"
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
        bot.edit_message_text(f"🎯 *التحدي:*\n{l.get('exercise', '...')}", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
    elif data[0] == "sol":
        bot.edit_message_text(f"✅ *الحل:*\n`{l.get('solution', '...')}`", call.message.chat.id, call.message.message_id, parse_mode="Markdown")

def run_health():
    try: socketserver.TCPServer(("", 8000), http.server.SimpleHTTPRequestHandler).serve_forever()
    except: pass

if __name__ == "__main__":
    # تشغيل سيرفر الصحة للبينق (Ping)
    threading.Thread(target=run_health, daemon=True).start()
    
    # السطر المعدل ليتناسب مع نسخة سيرفرك
    bot.remove_webhook() 
    
    time.sleep(1)
    print("🚀 Bot is Online!")
    
    # تفعيل تخطي التحديثات القديمة من هنا لتجنب TypeError
    bot.infinity_polling(skip_pending=True)
