import os
import telebot
from google import genai # المكتبة الجديدة
import threading
import http.server
import socketserver

# الإعدادات
TOKEN = os.getenv("TELEGRAM_TOKEN")
AI_KEY = os.getenv("GEMINI_KEY")

bot = telebot.TeleBot(TOKEN)

# إعداد العميل الجديد (New Client)
client = genai.Client(api_key=AI_KEY)
MODEL_ID = "gemini-1.5-flash"

INSTRUCTION = "أنت مدرس بايثون محترف ولطيف. ابدأ من الصفر مع الطالب بلهجة سعودية."

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "مرحباً بك في Bot Empire! 🐍\nمعك مدربك الخاص، وش حاب نتعلم اليوم؟")

@bot.message_handler(func=lambda message: True)
def chat(message):
    try:
        # الطريقة الجديدة لاستدعاء التوليد
        response = client.models.generate_content(
            model=MODEL_ID,
            contents=f"{INSTRUCTION}\nالطالب يقول: {message.text}"
        )
        
        if response.text:
            bot.send_message(message.chat.id, response.text)
        else:
            bot.send_message(message.chat.id, "الرد فارغ، جرب تسأل سؤال ثاني.")
            
    except Exception as e:
        print(f"حدث خطأ أثناء التوليد: {e}")
        bot.send_message(message.chat.id, "واجهت مشكلة في معالجة طلبك، حاول لاحقاً.")

# سيرفر الصحة (Health Check) لمنصة Koyeb
def run_health_server():
    port = 8000
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"Health check server ready on port {port}")
        httpd.serve_forever()

threading.Thread(target=run_health_server, daemon=True).start()

# تشغيل البوت مع تنظيف الـ Webhook لتجنب خطأ 409 Conflict
if __name__ == "__main__":
    print("Bot Empire is starting...")
    bot.remove_webhook()
    # استخدام infinity_polling لضمان استمرارية العمل
    bot.infinity_polling(timeout=20, long_polling_timeout=10)
