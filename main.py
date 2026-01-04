import os
import telebot
import google.generativeai as genai
import threading
import http.server
import socketserver

# جلب المفاتيح من البيئة
TOKEN = os.getenv("TELEGRAM_TOKEN")
AI_KEY = os.getenv("GEMINI_KEY")

bot = telebot.TeleBot(TOKEN)

# إعداد الـ AI
genai.configure(api_key=AI_KEY)

# استخدام الموديل الأحدث والأكثر استقراراً
# لاحظ أننا استخدمنا gemini-1.5-flash
model = genai.GenerativeModel('gemini-1.5-flash')

INSTRUCTION = "أنت مدرس بايثون محترف ولطيف. ابدأ من الصفر حتى الاحترااف و بشكل عفوي و تعليمي مع الطالب بلهجة سعودية محببة."

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "مرحبا بك في Bot Empire! 🐍✨\nأنا معلمك الخاص للبايثون، جاهز نبدأ؟")

@bot.message_handler(func=lambda message: True)
def chat(message):
    try:
        # توليد المحتوى مع معالجة الأخطاء
        full_prompt = f"{INSTRUCTION}\nالطالب يقول: {message.text}"
        response = model.generate_content(full_prompt)
        
        if response.text:
            bot.send_message(message.chat.id, response.text)
        else:
            bot.send_message(message.chat.id, "لم أستطع فهم ذلك، حاول صياغة السؤال بشكل آخر.")
            
    except Exception as e:
        print(f"حدث خطأ: {e}")
        # رسالة تنبيه للمستخدم بوجود مشكلة تقنية
        bot.send_message(message.chat.id, "أعتذر منك، واجهت مشكلة في الاتصال بعقلي الاصطناعي!")

# سيرفر فحص الحالة (Health Check)
def run_health_server():
    port = 8000
    handler = http.server.SimpleHTTPRequestHandler
    try:
        with socketserver.TCPServer(("", port), handler) as httpd:
            print(f"Health server running on port {port}")
            httpd.serve_forever()
    except Exception as e:
        print(f"Server error: {e}")

threading.Thread(target=run_health_server, daemon=True).start()

# تشغيل البوت
print("Bot is running...")
bot.polling(none_stop=True)
