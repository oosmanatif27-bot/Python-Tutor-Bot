import os
import telebot
import google.generativeai as genai
import threading
import http.server
import socketserver
import time

TOKEN = os.getenv("TELEGRAM_TOKEN")
AI_KEY = os.getenv("GEMINI_KEY")

# إعداد البوت
bot = telebot.TeleBot(TOKEN)
genai.configure(api_key=AI_KEY)
model = genai.GenerativeModel('gemini-1.5-flash') # تم تحديث الموديل

INSTRUCTION = """أنت مدرس بايثون محترف ولطيف. ابدأ مع الطالب من الصفر تماماً."""

@bot.message_handler(commands=['start'])
def send_welcome(message):
    # استخدام send_message بدل reply_to لتجنب خطأ 400
    bot.send_message(message.chat.id, "مرحبا صديقي! أنا مدرس البايثون الخاص فيك. جاهز نبدأ؟ أرسل 'ابدأ' 🐍✨")

@bot.message_handler(func=lambda message: True)
def chat(message):
    try:
        response = model.generate_content(f"{INSTRUCTION}\nالطالب يقول: {message.text}")
        # استخدام send_message هنا أيضاً للأمان
        bot.send_message(message.chat.id, response.text)
    except Exception as e:
        print(f"AI Error: {e}")

# كود المنفذ 8000 لإرضاء Koyeb
def run_health_server():
    port = 8000
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
        httpd.serve_forever()

threading.Thread(target=run_health_server, daemon=True).start()

# تشغيل البوت مع تخطي الأخطاء القديمة
bot.infinity_polling(timeout=10, long_polling_timeout=5)
