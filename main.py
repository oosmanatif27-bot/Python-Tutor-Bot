import os
import telebot
import google.generativeai as genai
import os 
# إعدادات الـ API (بنعلمك كيف تحطها بأمان بعدين)
TOKEN = "8362864755:AAHpwQGv98HckxteHT36Lnx6CtNXZXUl_7E"
AI_KEY = "AIzaSyAf34vpycvpBBquZG9lCMLiff4B3kEXuJ8"

import os
TOKEN = os.getenv("TELEGRAM_TOKEN")
AI_KEY = os.getenv("GEMINI_KEY")

bot = telebot.TeleBot(TOKEN)
genai.configure(api_key=AI_KEY)
model = genai.GenerativeModel('gemini-pro')

# نظام التدريس المنطقي اللي طلبته
INSTRUCTION = """أنت مدرس بايثون محترف ولطيف. 
ابدأ مع الطالب من الصفر تماماً. 
كل درس يجب أن يحتوي على: 1- شرح مبسط، 2- مثال كود، 3- تمرين برمجي.
إذا طلب الطالب تخطي التمرين، حذره بوضوح أن التخطّي قد يصعّب عليه الفهم لاحقاً، لكن قل له 'أنت حر' وانتقل للدرس التالي."""

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "مرحبا صديقي أنا مدرس البايثون الخاص فيك. جاهز نبدأ من الصفر؟ أرسل 'ابدأ' 🐍✨")

@bot.message_handler(func=lambda message: True)
def chat(message):
    # إرسال الكلام للـ AI للحصول على الرد
    response = model.generate_content(f"{INSTRUCTION}\nالطالب يقول: {message.text}")
    bot.reply_to(message, response.text)

bot.polling()