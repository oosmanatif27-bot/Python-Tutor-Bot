import os
import telebot
from telebot import types
import threading
import http.server
import socketserver

# جلب التوكن
TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = telebot.TeleBot(TOKEN)

# --- قاعدة بيانات الـ 12 درساً (المنهج الاحترافي) ---
lessons_data = {
    "1": {
        "title": "الدرس 1: دالة print",
        "explanation": "تخيل إن عندك ببغاء سحري 🦜، أي شيء تكتبه له بين قوسين `()` وعلامات تنصيص `\" \"` بياخذه ويصرخ به للعالم! هذه هي وظيفة `print`.",
        "exercise": "التمرين: حاول تخلي الببغاء يطبع اسمك (عثمان) باستخدام الكود.",
        "solution": "`print(\"عثمان\")`"
    },
    "2": {
        "title": "الدرس 2: المتغيرات (Variables)",
        "explanation": "المتغير مثل 'صندوق ألعاب' 📦 ملوّن. بتعطي الصندوق اسم (مثل `box`) وتحط داخله قيمة. لما تنادي اسم الصندوق، تطلع لك القيمة!",
        "exercise": "التمرين: اصنع صندوقاً اسمه `apples` وحط داخله رقم 3.",
        "solution": "`apples = 3`"
    },
    "3": {
        "title": "الدرس 3: العمليات الحسابية (Math Operators)",
        "explanation": "بايثون شاطرة جداً في الحساب ➕➖. تقدر تستخدمها كآلة حاسبة تجمع الحلويات أو تطرحها.",
        "exercise": "التمرين: اكتب كود يجمع 5 و 10.",
        "solution": "`print(5 + 10)`"
    },
    "4": {
        "title": "الدرس 4: المدخلات (User Input)",
        "explanation": "كيف تسأل البرنامج سؤال؟ نستخدم `input`. البرنامج بيوقف وينتظرك ترد عليه!",
        "exercise": "التمرين: اسأل المستخدم عن اسمه وخزنه في متغير اسمه `user_name`.",
        "solution": "`user_name = input(\"ما اسمك؟ \")`"
    },
    "5": {
        "title": "الدرس 5: القوائم (Lists)",
        "explanation": "تخيل حقيبة أدوات 🎒 تقدر تحط فيها أشياء كثيرة جنب بعض. هذي هي الـ List في بايثون.",
        "exercise": "التمرين: اصنع قائمة اسمها `fruits` فيها 'تفاح' و 'موز'.",
        "solution": "`fruits = [\"تفاح\", \"موز\"]`"
    },
    "6": {
        "title": "الدرس 6: القواميس (Dictionaries)",
        "explanation": "مثل دفتر العناوين 📖؛ تحط 'الاسم' وجنبه 'الرقم'. نظام (مفتاح وقيمة).",
        "exercise": "التمرين: اصنع قاموساً فيه اسمك `\"name\": \"عثمان\"`.",
        "solution": "`data = {\"name\": \"عثمان\"}`"
    },
    "7": {
        "title": "الدرس 7: الجمل الشرطية (If Statements)",
        "explanation": "مثل إشارة المرور 🚦؛ 'لو' اللون أحمر قف، 'لو' أخضر امشي. البرنامج يتخذ قرار بناءً على شرط.",
        "exercise": "التمرين: اكتب شرطاً يطبع 'ناجح' إذا كان `score` أكبر من 50.",
        "solution": "```python\nif score > 50:\n    print(\"ناجح\")```"
    },
    "8": {
        "title": "الدرس 8: الحلقات التكرارية (Loops)",
        "explanation": "بدل ما تكرر الكود 100 مرة، الـ Loop مثل 'الآلة المكررة' 🔄 تسويها عنك في سطرين.",
        "exercise": "التمرين: اجعل البرنامج يطبع كلمة 'أهلاً' 3 مرات باستخدام `range`.",
        "solution": "```python\nfor i in range(3):\n    print(\"أهلاً\")```"
    },
    "9": {
        "title": "الدرس 9: الدوال (Functions)",
        "explanation": "هذا 'مصنع أكواد' 🏭. تصنع كود وتعطيه اسم (مثل `def`) وتستخدمه في أي وقت تبيه.",
        "exercise": "التمرين: اصنع دالة اسمها `say_hi` تطبع 'مرحباً'.",
        "solution": "```python\ndef say_hi():\n    print(\"مرحباً\")```"
    },
    "10": {
        "title": "الدرس 10: معالجة الأخطاء (Error Handling)",
        "explanation": "لو انكسرت اللعبة 🛠️، بنستخدم `try` و `except` عشان البرنامج ما يوقف ويقول لنا وش المشكلة بهدوء.",
        "exercise": "التمرين: جرب تقسيم 10 على 0 داخل `try`.",
        "solution": "```python\ntry:\n    print(10/0)\nexcept:\n    print(\"خطأ!\")```"
    },
    "11": {
        "title": "الدرس 11: الملفات (Files)",
        "explanation": "كيف تخلي البرنامج يكتب ذكرياته في 'دفتر مذكرات' 📝 (ملف خارجي) ويقرأ منها بعدين؟",
        "exercise": "التمرين: افتح ملفاً اسمه `notes.txt` واكتب فيه 'مرحباً'.",
        "solution": "`with open(\"notes.txt\", \"w\") as f: f.write(\"مرحباً\")`"
    },
    "12": {
        "title": "الدرس 12: المكتبات (Modules)",
        "explanation": "بايثون عندها 'صندوق ألعاب جاهزة' 🎁 صنعها مبرمجون آخرون. استخدم `import` لتلعب بها!",
        "exercise": "التمرين: استخدم مكتبة `random` لطباعة رقم عشوائي.",
        "solution": "`import random\nprint(random.randint(1,10))`"
    }
}

# --- نظام معالجة الرسائل ---

@bot.message_handler(commands=['start'])
def welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(types.KeyboardButton("مقدمة بايثون"), types.KeyboardButton("قائمة الدروس"))
    msg = "👋 هلا بك في **Bot Empire**!\nمدربك الذكي لتعلم بايثون بأسلوب سهل وممتع.\n\nاختر من الأزرار بالأسفل لنبدأ:"
    bot.send_message(message.chat.id, msg, reply_markup=markup, parse_mode="Markdown")

@bot.message_handler(func=lambda m: m.text == "مقدمة بايثون")
def intro(message):
    text = """تعد لغة بايثون واحدة من أشهر وأقوى لغات البرمجة في العالم، صُممت لتكون سهلة القراءة وبسيطة مثل اللغة الإنجليزية. أصبحت اليوم الركيزة الأساسية في مجالات الذكاء الاصطناعي، تطوير الويب، والأمن السيبراني."""
    bot.send_message(message.chat.id, text)

@bot.message_handler(func=lambda m: m.text == "قائمة الدروس")
def show_curriculum(message):
    markup = types.InlineKeyboardMarkup(row_width=4)
    btns = [types.InlineKeyboardButton(text=f"L{i}", callback_data=f"lesson_{i}") for i in range(1, 13)]
    markup.add(*btns)
    bot.send_message(message.chat.id, "📚 **خارطة الطريق الخاصة بك:**\nاختر الدرس الذي تود تعلمه الآن:", reply_markup=markup, parse_mode="Markdown")

# --- معالجة الأزرار الشفافة ---
@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    data = call.data
    
    if data.startswith("lesson_"):
        l_id = data.split("_")[1]
        lesson = lessons_data[l_id]
        text = f"💡 *{lesson['title']}*\n\n{lesson['explanation']}"
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🎯 ابدأ التحدي", callback_data=f"ex_{l_id}"))
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif data.startswith("ex_"):
        l_id = data.split("_")[1]
        lesson = lessons_data[l_id]
        text = f"🎯 *التحدي:*\n{lesson['exercise']}"
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🔑 كشف الحل", callback_data=f"sol_{l_id}"))
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif data.startswith("sol_"):
        l_id = data.split("_")[1]
        lesson = lessons_data[l_id]
        text = f"✅ *الحل الصحيح:*\n{lesson['solution']}\n\nأنت مبرمج ذكي جداً! 🚀 واصل تقدمك."
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode="Markdown")

# --- Health Check لـ Koyeb ---
def run_health():
    socketserver.TCPServer(("", 8000), http.server.SimpleHTTPRequestHandler).serve_forever()

threading.Thread(target=run_health, daemon=True).start()

# --- التشغيل النهائي ---
if __name__ == "__main__":
    bot.remove_webhook()
    print("Bot is LIVE and Running...")
    bot.infinity_polling(skip_pending=True)
