import os, telebot, threading, http.server, socketserver
from telebot import types

TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = telebot.TeleBot(TOKEN)

# --- قاعدة البيانات العلمية المنسقة ---
lessons_data = {
    "1": {
        "title": "الدرس 1: دالة print (الإخراج)",
        "explanation": "هذه الدالة هي لسان البرمجة. نستخدمها لعرض النتائج.\n• للنصوص (String): نضعها بين `\" \"` مثل: `print(\"هلا\")`.\n• للأرقام (Integer): نكتبها مباشرة مثل: `print(100)`.\n• للدمج: نستخدم الفاصلة `,` بين النص والرقم.",
        "exercise": "اكتب كود يطبع كلمة 'المستوى' وجنبها رقم 1.",
        "solution": "`print(\"المستوى\", 1)`"
    },
    "2": {
        "title": "الدرس 2: المتغيرات (Variables)",
        "explanation": "هي أماكن في الذاكرة نحجزها لنخزن فيها قيم (نصوص أو أرقام) لنناديها لاحقاً باسمها.\nمثال: `score = 50` (حفظنا الرقم 50 في متغير اسمه score).",
        "exercise": "اصنع متغير باسم `name` وضع فيه اسمك كنص (String).",
        "solution": "`name = \"عثمان\"`"
    },
    "3": {
        "title": "الدرس 3: العمليات الحسابية (Operators)",
        "explanation": "بايثون تنفذ العمليات الحسابية بدقة. `+` للجمع، `-` للطرح، `*` للضرب، و `/` للقسمة.",
        "exercise": "اكتب كود يطبع حاصل ضرب 5 في 4.",
        "solution": "`print(5 * 4)`"
    },
    # ... (باقي الدروس الـ 12 تتبع نفس النمط العلمي المبسط)
}

@bot.message_handler(commands=['start'])
def welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add("مقدمة بايثون", "قائمة الدروس")
    bot.send_message(message.chat.id, "🚀 أهلاً بك في أكاديمية بايثون.\nاختر 'قائمة الدروس' لتبدأ رحلتك العلمية:", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text == "مقدمة بايثون")
def intro(message):
    text = """تُعد بايثون (Python) لغة برمجة عالية المستوى (High-level)، مفسرة (Interpreted)، وسهلة القراءة. تعتمد على الإزاحة (Indentation) لتنظيم الكود بدلاً من الأقواس المعقدة، مما يجعلها المفضلة للمبتدئين والخبراء في الذكاء الاصطناعي."""
    bot.send_message(message.chat.id, text)

@bot.message_handler(func=lambda m: m.text == "قائمة الدروس")
def list_lessons(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    btns = [types.KeyboardButton(f"الدرس {i}") for i in range(1, 13)]
    markup.add(*btns, types.KeyboardButton("الرجوع للقائمة الرئيسية"))
    bot.send_message(message.chat.id, "📚 اختر الدرس:", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text.startswith("الدرس "))
def open_lesson(message):
    num = message.text.split()[-1]
    if num in lessons_data:
        l = lessons_data[num]
        text = f"💡 *{l['title']}*\n\n{l['explanation']}"
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🎯 تحدي الدرس", callback_data=f"ex_{num}"))
        bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    l_id = call.data.split("_")[1]
    l = lessons_data[l_id]
    if call.data.startswith("ex_"):
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🔑 الحل العلمي", callback_data=f"sol_{l_id}"))
        bot.edit_message_text(f"🎯 *التحدي:*\n{l['exercise']}", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
    elif call.data.startswith("sol_"):
        bot.edit_message_text(f"✅ *الحل ككود بايثون:*\n{l['solution']}\n\nاستمر في التعلم! 🚀", call.message.chat.id, call.message.message_id, parse_mode="Markdown")

def run_health():
    try: socketserver.TCPServer(("", 8000), http.server.SimpleHTTPRequestHandler).serve_forever()
    except: pass

threading.Thread(target=run_health, daemon=True).start()

if __name__ == "__main__":
    bot.remove_webhook()
    bot.infinity_polling(skip_pending=True)
