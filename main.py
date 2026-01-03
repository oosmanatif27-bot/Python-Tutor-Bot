import os
import telebot
import google.generativeai as genai
import threading
import http.server
import socketserver

# إعدادات الرموز السرية
TOKEN = os.getenv("TELEGRAM_TOKEN")
AI_KEY = os.getenv("GEMINI_KEY")

bot = telebot.TeleBot(TOKEN)
genai.configure(api_key=AI_KEY)

# --- تصحيح اسم الموديل هنا ---
model = genai.GenerativeModel('gemini-1.5-flash') 

INSTRUCTION = """أنت مدرس بايثون محترف ولطيف. 
ابدأ مع الطالب من الصفر تماماً. 
كل درس يجب أن يحتوي على: 1- شرح مبسط، 2- مثال كود، 3- تمرين برمجي.
إذا طلب الطالب تخطي التمرين، حذره بوضوح أن التخطّي قد يصعّب عليه الفهم لاحقاً، لكن قل له 'أنت حر' وانتقل للدرس التالي."""

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "مرحبا صديقي أنا مدرس البايثون الخاص فيك. جاهز نبدأ من الصفر؟ أرسل 'ابدأ' 🐍✨")

@bot.message_handler(func=lambda message: True)
def chat(message):
    try:
        response = model.generate_content(f"{INSTRUCTION}\nالطالب يقول: {message.text}")
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, "حصل خطأ بسيط في الاتصال بالذكاء الاصطناعي، جرب مرة ثانية.")

# --- كود حل مشكلة Port 8000 في Koyeb ---
def run_health_server():
    port = 8000
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
        httpd.serve_forever()

threading.Thread(target=run_health_server, daemon=True).start()

bot.polling()
