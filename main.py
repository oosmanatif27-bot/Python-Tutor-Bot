import os
import telebot
import google.generativeai as genai
import threading
import http.server
import socketserver

TOKEN = os.getenv("TELEGRAM_TOKEN")
AI_KEY = os.getenv("GEMINI_KEY")

bot = telebot.TeleBot(TOKEN)
genai.configure(api_key=AI_KEY)

# تأكد من وجود models/ قبل اسم الموديل
model = genai.GenerativeModel('models/gemini-1.5-flash') 

INSTRUCTION = """أنت مدرس بايثون محترف ولطيف. ابدأ من الصفر."""

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "مرحبا صديقي! جاهز؟ أرسل 'ابدأ' 🐍✨")

@bot.message_handler(func=lambda message: True)
def chat(message):
    try:
        response = model.generate_content(f"{INSTRUCTION}\nالطالب يقول: {message.text}")
        bot.send_message(message.chat.id, response.text)
    except Exception as e:
        print(f"Error: {e}")

def run_health_server():
    port = 8000
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
        httpd.serve_forever()

threading.Thread(target=run_health_server, daemon=True).start()

# السطر اللي كان فيه المشكلة.. تأكد من القوس في آخره!
bot.polling(none_stop=True, timeout=90, long_polling_timeout=90)
