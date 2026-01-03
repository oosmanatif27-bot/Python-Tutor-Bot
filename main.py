import os
import telebot
import google.generativeai as genai
import threading
import http.server
import socketserver
import time

# إعدادات الرموز السرية
TOKEN = os.getenv("TELEGRAM_TOKEN")
AI_KEY = os.getenv("GEMINI_KEY")

# إعداد البوت مع زيادة وقت الانتظار (Timeout) لحل مشكلة السجلات
bot = telebot.TeleBot(TOKEN, threaded=True)
genai.configure(api_key=AI_KEY)

# --- التعديل الأهم: تغيير الموديل لنسخة 1.5 ---
model = genai.GenerativeModel('gemini-1.5-flash') 

INSTRUCTION = """أنت مدرس بايثون محترف ولطيف. ابدأ مع الطالب من الصفر تماماً."""

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "مرحبا! أنا مدرس البايثون الخاص فيك. أرسل 'ابدأ' لننطلق 🐍")

@bot.message_handler(func=lambda message: True)
def chat(message):
    try:
        response = model.generate_content(f"{INSTRUCTION}\nالطالب يقول: {message.text}")
        bot.reply_to(message, response.text)
    except Exception as e:
        print(f"Error: {e}")
        bot.reply_to(message, "الذكاء الاصطناعي مشغول شوي، جرب ترسل رسالتك مرة ثانية.")

# --- حل مشكلة المنفذ 8000 في Koyeb ---
def run_health_server():
    port = 8000
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
        httpd.serve_forever()

threading.Thread(target=run_health_server, daemon=True).start()

# تشغيل البوت مع محاولة إعادة الاتصال تلقائياً عند حدوث Timeout
while True:
    try:
        bot.polling(none_stop=True, timeout=60)
    except Exception as e:
        print(f"Polling error: {e}")
        time.sleep(5)
