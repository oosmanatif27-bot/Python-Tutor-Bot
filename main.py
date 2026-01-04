import os
import telebot
from telebot import types
import threading
import http.server
import socketserver

TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = telebot.TeleBot(TOKEN)

# --- قاموس المنهج الشامل (Bot Empire Curriculum) ---

curriculum = {
    "مقدمة": (
        "🌟 **لماذا بايثون؟**\n\n"
        "بايثون هي اللغة رقم 1 في الأمن السيبراني والذكاء الاصطناعي. سهلة كأنك تكتب إنجليزي.\n"
        "فرقها عن غيرها؟ ما تحتاج تعقيد، سطر واحد في بايثون يعادل 10 سطور في لغات ثانية!\n"
        "📚 **كتب ننصح بها:** Python Crash Course."
    ),
    "1": (
        "📖 **الدرس 1: دالة الطباعة (print)**\n\n"
        "هي وسيلة تواصل البرنامج معك. أي شيء داخل `print()` يظهر على الشاشة.\n"
        "**مثال:** `print('Hello Hacker')`"
    ),
    "2": (
        "📖 **الدرس 2: المتغيرات وأنواع البيانات**\n\n"
        "المتغيرات هي صناديق تخزن بيانات. أنواعها:\n"
        "1. **Integer:** أرقام صحيحة مثل `x = 5`\n"
        "2. **String:** نصوص مثل `name = 'Neno'`\n"
        "3. **Float:** أرقام بفاصلة مثل `pi = 3.14`"
    ),
    "3": (
        "📖 **الدرس 3: هياكل البيانات (Data Structures)**\n\n"
        "كيف ننظم بيانات كثيرة؟\n"
        "- **List (القائمة):** صندوق كبير فيه أغراض مرتبة: `tools = ['nmap', 'sqlmap']`\n"
        "- **Dictionary (القاموس):** مفتاح وقيمة: `user = {'id': 1, 'name': 'admin'}`"
    ),
    "4": (
        "📖 **الدرس 4: الجمل الشرطية (Control Flow)**\n\n"
        "هنا تجعل برنامجك ذكي ويتخذ قرارات باستخدام `if`.\n"
        "**مثال:**\n"
        "```python\n"
        "password = '123'\n"
        "if password == '123':\n"
        "    print('Access Granted')\n"
        "else:\n"
        "    print('Access Denied')\n"
        "```"
    ),
    "5": (
        "📖 **الدرس 5: الحلقات التكرارية (Loops)**\n\n"
        "بدل ما تكرر الكود 100 مرة، استخدم Loop!\n"
        "- **For loop:** للمرور على قائمة.\n"
        "- **While loop:** للتكرار طالما الشرط صحيح.\n"
        "**مثال:** `for i in range(5): print(i)`"
    ),
    "6": (
        "📖 **الدرس 6: الدوال (Functions)**\n\n"
        "الدالة هي كود تغلفه باسم عشان تستخدمه كل شوي بدل ما تعيد كتابته.\n"
        "**مثال:**\n"
        "```python\n"
        "def greet():\n"
        "    print('Welcome to Bot Empire')\n"
        "\n"
        "greet() # استدعاء الدالة\n"
        "```"
    ),
    "7": (
        "📖 **الدرس 7: التعامل مع الملفات (File I/O)**\n\n"
        "كيف يقرأ البوت ملفات أو يكتب فيها؟\n"
        "استخدم `open()`.\n"
        "**مثال للكتّابة:**\n"
        "`with open('passwords.txt', 'w') as f: f.write('secret')`"
    ),
    "8": (
        "📖 **الدرس 8: المكتبات والوحدات (Modules)**\n\n"
        "لا تخترع العجلة! استخدم أكواد جاهزة.\n"
        "مثلاً مكتبة `os` للتعامل مع النظام، أو `requests` للإنترنت.\n"
        "تستدعيها بكلمة: `import`"
    )
}

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btns = [types.KeyboardButton("مقدمة"), types.KeyboardButton("الدرس 1"), 
            types.KeyboardButton("الدرس 2"), types.KeyboardButton("الدرس 3"),
            types.KeyboardButton("الدرس 4"), types.KeyboardButton("الدرس 5"),
            types.KeyboardButton("الدرس 6"), types.KeyboardButton("الدرس 7"),
            types.KeyboardButton("الدرس 8")]
    markup.add(*btns)
    
    bot.send_message(message.chat.id, 
                     "مرحباً بك في **Bot Empire** 🐍\nأنا مدربك الخاص. اختر درساً لنبدأ الرحلة:", 
                     reply_markup=markup, parse_mode="Markdown")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    text = message.text
    if "مقدمة" in text:
        bot.send_message(message.chat.id, curriculum["مقدمة"], parse_mode="Markdown")
    elif "الدرس" in text:
        num = text.split()[-1]
        if num in curriculum:
            bot.send_message(message.chat.id, curriculum[num], parse_mode="Markdown")
        else:
            bot.send_message(message.chat.id, "هذا الدرس قيد التحضير!")
    else:
        bot.send_message(message.chat.id, "اختر درساً من القائمة بالأسفل يا بطل 👇")

# --- Health Server for Koyeb ---
def run_health_server():
    port = 8000
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
        httpd.serve_forever()

threading.Thread(target=run_health_server, daemon=True).start()

if __name__ == "__main__":
    bot.remove_webhook()
    print("Bot Empire Academy is live!")
    bot.infinity_polling()
