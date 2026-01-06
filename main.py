import os
import telebot
from telebot import types
import threading
import http.server
import socketserver

# جلب التوكن
TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = telebot.TeleBot(TOKEN)

# --- قاعدة بيانات الـ 12 درساً ---
lessons_data = {
    "1": {"title": "الدرس 1: print", "explanation": "تخيل إن عندك ببغاء سحري 🦜، أي شيء تكتبه له بين قوسين بيكرره!", "exercise": "اطبع اسمك باستخدام الكود.", "solution": "`print('عثمان')`"},
    "2": {"title": "الدرس 2: Variables", "explanation": "المتغير مثل صندوق ألعاب 📦 بتعطيه اسم وتحط فيه قيمة.", "exercise": "اصنع صندوقاً اسمه apples وحط فيه 5.", "solution": "`apples = 5`"},
    "3": {"title": "الدرس 3: Math", "explanation": "بايثون آلة حاسبة ذكية ➕➖.", "exercise": "اجمع 10 و 20.", "solution": "`print(10 + 20)`"},
    "4": {"title": "الدرس 4: Input", "explanation": "كيف تسأل المستخدم سؤال؟ نستخدم `input`.", "exercise": "اسأل المستخدم عن عمره.", "solution": "`age = input('كم عمرك؟')`"},
    "5": {"title": "الدرس 5: Lists", "explanation": "حقيبة أدوات 🎒 تحط فيها أشياء كثيرة.", "exercise": "اصنع قائمة فيها 'موز' و 'تفاح'.", "solution": "`list = ['موز', 'تفاح']`"},
    "6": {"title": "الدرس 6: Dictionaries", "explanation": "دفتر عناوين 📖 يحفظ الاسم وجنبه الرقم.", "exercise": "اصنع قاموساً يحمل اسمك.", "solution": "`d = {'name': 'عثمان'}`"},
    "7": {"title": "الدرس 7: If Statements", "explanation": "مثل إشارة المرور 🚦؛ تتخذ قرار بناءً على اللون.", "exercise": "اكتب شرطاً لو x أكبر من 5 يطبع 'كبير'.", "solution": "if x > 5: print('كبير')"},
    "8": {"title": "الدرس 8: Loops", "explanation": "آلة تكرار 🔄 تكرر الكود عنك.", "exercise": "اطبع 'هلا' 3 مرات.", "solution": "for i in range(3): print('هلا')"},
    "9": {"title": "الدرس 9: Functions", "explanation": "مصنع أكواد 🏭 تعطيه اسم وتستخدمه دائماً.", "exercise": "عرف دالة اسمها hi.", "solution": "def hi(): print('هلا')"},
    "10": {"title": "الدرس 10: Errors", "explanation": "كيف نصلح اللعبة لو خربت 🛠️ باستخدام try.", "exercise": "جرب كود تقسيم 5 على 0.", "solution": "try: 5/0 \nexcept: print('خطأ')"},
    "11": {"title": "الدرس 11: Files", "explanation": "الكتابة في دفتر مذكرات 📝 (ملفات txt).", "exercise": "افتح ملفاً للكتابة.", "solution": "open('file.txt', 'w')"},
    "12": {"title": "الدرس 12: Modules", "explanation": "استخدام ألعاب جاهزة 🎁 بكلمة import.", "exercise": "استورد مكتبة random.", "solution": "import random"}
}

# --- نظام معالجة الرسائل ---

@bot.message_handler(commands=['start'])
def welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(types.KeyboardButton("مقدمة بايثون"), types.KeyboardButton("قائمة الدروس"))
    bot.send_message(message.chat.id, "👋 هلا بك! اختر من الأزرار بالأسفل:", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text == "مقدمة بايثون")
def intro(message):
    # النص الطويل باستخدام الثلاث علامات لتجنب الـ SyntaxError
    text = """تُعد بايثون لغة برمجة عالية المستوى، تمتاز بفلسفة "سهولة القراءة" والقوة في التنفيذ. هي اللغة رقم 1 حالياً في العالم للذكاء الاصطناعي والأمن السيبراني."""
    bot.send_message(message.chat.id, text)

@bot.message_handler(func=lambda m: m.text == "قائمة الدروس")
def show_lessons_keyboard(message):
    # رجعنا الأزرار كيبورد عادي مثل ما طلبت
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    btns = [types.KeyboardButton(f"الدرس {i}") for i in range(1, 13)]
    markup.add(*btns)
    markup.add(types.KeyboardButton("الرجوع للقائمة الرئيسية"))
    bot.send_message(message.chat.id, "📚 اختر الدرس الذي تريد تعلمه:", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text == "الرجوع للقائمة الرئيسية")
def back_home(message):
    welcome(message)

@bot.message_handler(func=lambda m: m.text.startswith("الدرس "))
def handle_lesson_selection(message):
    num = message.text.split()[-1]
    if num in lessons_data:
        lesson = lessons_data[num]
        text = f"💡 *{lesson['title']}*\n\n{lesson['explanation']}"
        # هنا تظهر أزرار التمرين والحل داخل الرسالة
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🎯 ابدأ التحدي", callback_data=f"ex_{num}"))
        bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: True)
def handle_inline_buttons(call):
    l_id = call.data.split("_")[1]
    lesson = lessons_data[l_id]
    
    if call.data.startswith("ex_"):
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🔑 كشف الحل", callback_data=f"sol_{l_id}"))
        bot.edit_message_text(f"🎯 *التحدي:*\n{lesson['exercise']}", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
    
    elif call.data.startswith("sol_"):
        bot.edit_message_text(f"✅ *الحل:*\n{lesson['solution']}\n\nأنت مبرمج بطل! 🚀", call.message.chat.id, call.message.message_id, parse_mode="Markdown")

# --- Health Check لـ Koyeb ---
def run_health():
    try: socketserver.TCPServer(("", 8000), http.server.SimpleHTTPRequestHandler).serve_forever()
    except: pass

threading.Thread(target=run_health, daemon=True).start()

if __name__ == "__main__":
    bot.remove_webhook()
    bot.infinity_polling(skip_pending=True)
