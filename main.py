import os
import telebot
import google.generativeai as genai
import threading
import http.server
import socketserver
import time

# 1. إعداد الرموز السرية (تأكد إنك ضايفهم في Koyeb Environment Variables)
TOKEN = os.getenv("TELEGRAM_TOKEN")
AI_KEY = os.getenv("GEMINI_KEY")

# 2. إعداد البوت والموديل (استخدام النسخة المستقرة)
bot = telebot.TeleBot(TOKEN)
genai.configure(api_key=AI_KEY)
model = genai.GenerativeModel('models/gemini-1.5-flash')
# 3. نظام التدريس (التعليمات البرمجية)
INSTRUCTION = """أنت مدرس بايثون محترف ولطيف. 
ابدأ مع الطالب من الصفر تماماً. 
كل درس يجب أن يحتوي على: 1- شرح مبسط، 2- مثال كود، 3- تمرين برمجي.
إذا طلب الطالب تخطي التمرين، حذره بوضوح أن التخطّي قد يصعّب عليه الفهم لاحقاً، لكن قل له 'أنت حر' وانتقل للدرس التالي."""

# 4. الرد على أمر /start (رسالة الترحيب اللي كنت تبيها)
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "مرحبا صديقي! أنا مدرس البايثون الخاص فيك. جاهز نبدأ من الصفر؟ أرسل 'ابدأ' 🐍✨")

# 5. معالجة الرسائل والدردشة مع الذكاء الاصطناعي
@bot.message_handler(func=lambda message: True)
def chat(message):
    try:
        # إرسال النص للموديل
        response = model.generate_content(f"{INSTRUCTION}\nالطالب يقول: {message.text}")
        bot.send_message(message.chat.id, response.text)
    except Exception as e:
        print(f"خطأ في الذكاء الاصطناعي: {e}")
        bot.send_message(message.chat.id, "معليش يا بطل، فيه ضغط على السيرفر، جرب ترسل مرة ثانية.")

# 6. حل مشكلة Port 8000 لخدمة Koyeb (عشان ما يعطيك Error أحمر)
def run_health_server():
    port = 8000
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
        httpd.serve_forever()

# تشغيل سيرفر الصحة في الخلفية
threading.Thread(target=run_health_server, daemon=True).start()

# 7. تشغيل البوت مع ميزة skip_pending لتجنب تعليق الرسائل القديمة
print("البوت بدأ العمل بنجاح...")
bot.infinity_polling(skip_pending=True)

