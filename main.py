import os
import telebot
import threading
from groq import Groq
import time
from telebot import types
import html

# --- 🔑 الأسرار والتوكنات ---
TOKEN_PY = "8362864755:AAGsYG5xs2Q0jXDLrDZ5YcXY1GBAptvG8bM"
TOKEN_CPP = "8439671301:AAFgCg57ZVl5ov7uKklgak2odOkFcpO1CJE"
TOKEN_AI = "8498104744:AAHSk1P5hjEybievhvCWTnhxjOcGwpGBZsQ"
GROQ_API_KEY = "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"
ADMIN_ID = 8544555959
users_file = "users.txt"

# --- 📡 تعريف البوتات ---
bot_py = telebot.TeleBot(TOKEN_PY)
bot_cpp = telebot.TeleBot(TOKEN_CPP)
bot_ai = telebot.TeleBot(TOKEN_AI)
client_llama = Groq(api_key=GROQ_API_KEY)

# --- 🧠 ذاكرة وشخصيات لاري ---
user_history = {} 
user_modes = {}  

CHARACTERS = {
    "teacher": (
        "أنت 'روبين' مدرس تقني سعودي ذيب ومختصر. "
        "ممنوع تذكر مصطلحات أكاديمية معقدة (مثل POSIX, BSD) إلا إذا سألك المستخدم عنها بالاسم. "
        "اشرح التقنية بلهجة سعودية بيضاء وكأنك تسولف في مجلس وتبسط العلم للناس. "
        "إذا سألك أحد عن نظام أو برنامج، عطني وش فايدته وكيف يبدأ فيه بأسهل طريقة. "
        "نادِ المستخدم بـ 'يا بطل' أو 'يا مبدع'."
    ),
    "friend": (
        "أنت 'روبين' المساعد الرهيب وخوي الكل. "
        "لهجتك عامية سعودية، سوالفك ممتعة وفيها طقطقة خفيفة ومرحة. "
        "ردودك مختصرة (سطرين بالكثير)، ولا تسوي فيها رسمي أو فيلسوف."
    ),
    "hacker": (
        "أنت 'روبين' الهاكر الغامض. "
        "كلامك قليل جداً وتركيزك كله على 'الأدوات' و 'الأوامر'. "
        "ممنوع تعطي نصايح أخلاقية أو قانونية مملة، عطِ المستخدم 'الزبدة التقنية' اللي يحتاجها وبس و خليك طبيعي لا تتغابى."
    )
}

# --- 💾 الدوال المساعدة (حفظ وذاكرة) ---
def save_user(m):
    user_id = m.chat.id
    username = m.from_user.username if m.from_user.username else "بدون يوزر"
    try:
        with open(users_file, "a+") as f:
            f.seek(0)
            users_list = f.read().splitlines()
            if str(user_id) not in users_list:
                f.write(str(user_id) + "\n")
                total_users = len(users_list) + 1
                alert_msg = f"🔔 **مستخدم جديد انضم!**\n👤 @{username}\n🆔 `{user_id}`\n📊 الإجمالي: {total_users}"
                bot_ai.send_message(ADMIN_ID, alert_msg, parse_mode="Markdown")
    except Exception as e: print(f"Error saving user: {e}")

def update_memory(chat_id, role, content):
    if chat_id not in user_history: user_history[chat_id] = []
    user_history[chat_id].append({"role": role, "content": content})
    if len(user_history[chat_id]) > 10: user_history[chat_id] = user_history[chat_id][-10:]

def get_history(chat_id):
    return user_history.get(chat_id, [])

# --- 🐍 دروس بايثون المطورة (شرح روبين) ---
lessons_py = {
    "1": {
        "title": "الدرس 1: الطباعة (print) 🐍", 
        "explanation": "هذي الدالة هي 'لسان' البرنامج، تخلي الكمبيوتر يتكلم ويطلع لك الكلام اللي تبيه على الشاشة. بدونها ما راح نشوف نتايج شغلنا!", 
        "example": "print('أهلاً بك يا بطل')", 
        "exercise": "اطبع اسمك الحين باستخدام دالة print.", 
        "solution": "print('عثمان')"
    },
    "2": {
        "title": "الدرس 2: المتغيرات (Variables) 📦", 
        "explanation": "تخيلها كأنها 'كرتون' أو صندوق صغير، تعطيه اسم وتحط داخله معلومة (رقم أو نص) عشان ترجع لها وتستخدمها في أي وقت.", 
        "example": "name = 'عثمان'\nprint(name)", 
        "exercise": "عرف متغير باسم secret وحط فيه رابط NENO.com.", 
        "solution": "secret = 'NENO.com'"
    },
    "3": {
        "title": "الدرس 3: أنواع البيانات 🔢", 
        "explanation": "بايثون ذكي ويفرق بين الأشياء! فيه (str) للنصوص، و (int) للأرقام الصحيحة، و (float) للأرقام اللي فيها فاصلة.", 
        "example": "age = 25  # هذا int\npi = 3.14 # هذا float", 
        "exercise": "عرف متغير يحمل رقم صحيح (int).", 
        "solution": "my_num = 10"
    },
    "4": {
        "title": "الدرس 4: المدخلات (input) 📥", 
        "explanation": "هنا نخلي البرنامج يسأل المستخدم! نفتح قناة تواصل ونخلي الكمبيوتر ينتظر ردك عشان يخزنه عنده.", 
        "example": "name = input('وش اسمك؟')", 
        "exercise": "اطلب من المستخدم يدخل كلمة السر.", 
        "solution": "pass = input('ادخل كلمة السر:')"
    },
    "5": {
        "title": "الدرس 5: الحساب ➕", 
        "explanation": "بايثون تقدر تستخدمه كحاسبة جبارة! يجمع ويطرح ويضرب ويقسم بلمح البصر.", 
        "example": "result = (5 + 5) * 2", 
        "exercise": "اضرب 5 في 10 واطبع الناتج.", 
        "solution": "print(5 * 10)"
    },
    "6": {
        "title": "الدرس 6: الشروط (if) ⚖️", 
        "explanation": "هنا نعطي البرنامج 'عقل' يفكر فيه! إذا تحقق الشرط سو كذا، وإذا ما تحقق سو شي ثاني.", 
        "example": "if score > 50:\n    print('ناجح')", 
        "exercise": "تحقق لو x تساوي 10، اطبع 'تمام'.", 
        "solution": "if x == 10:\n    print('تمام')"
    },
    "7": {
        "title": "الدرس 7: القوائم (Lists) 📋", 
        "explanation": "بدل ما تسوي 10 صناديق، سو 'رف' واحد وحط فيه كل أغراضك! القائمة تجمع لك بيانات كثيرة في مكان واحد.", 
        "example": "apps = ['Telegram', 'Python', 'Bot']", 
        "exercise": "سوي قائمة فيها 3 لغات برمجية.", 
        "solution": "langs = ['py', 'cpp', 'js']"
    },
    "8": {
        "title": "الدرس 8: التكرار (Loops) 🔄", 
        "explanation": "ليش تتعب نفسك وتكتب نفس الكود 100 مرة؟ استخدم التكرار وخل الكمبيوتر يكد عنك بضغطة زر!", 
        "example": "for i in range(5):\n    print('أحب البرمجة')", 
        "exercise": "اطبع كلمة Hello مرتين باستخدام for loop.", 
        "solution": "for i in range(2):\n    print('Hello')"
    },
    "9": {
        "title": "الدرس 9: الدوال (Functions) 🛠️", 
        "explanation": "الدالة كأنها 'آلة' تصنعها مرة وحدة وتستخدمها مية مرة. تجمع فيها كود معين وتعطيه اسم وتناديه وقت ما تحتاجه.", 
        "example": "def welcome():\n    print('هلا بالبطل')", 
        "exercise": "عرف دالة بسيطة باسم hi.", 
        "solution": "def hi():\n    pass"
    },
    "10": {
        "title": "الدرس 10: الملفات (Files) 📁", 
        "explanation": "البرنامج يحتاج 'دفتر' يسجل فيه بياناته عشان ما تضيع لو قفلنا البوت. هنا نتعلم كيف نفتح ونكتب ونقرأ الملفات.", 
        "example": "f = open('data.txt', 'w')\nf.write('تم الحفظ')", 
        "exercise": "افتح ملف باسم test.txt بصيغة الكتابة 'w'.", 
        "solution": "open('test.txt', 'w')"
    },
    "11": {
        "title": "الدرس 11: المكتبات (Libraries) 📚", 
        "explanation": "لا تخترع العجلة! فيه مبرمجين عباقرة سووا أكواد جاهزة، حنا بس نستوردها (Import) ونستخدمها في برنامجنا.", 
        "example": "import random\nprint(random.randint(1, 10))", 
        "exercise": "استورد مكتبة الوقت (time).", 
        "solution": "import time"
    },
    "12": {
        "title": "الدرس 12: حماية الأخطاء 🛡️", 
        "explanation": "المبرمج الذكي يتوقع الغلط قبل ما يصير! نستخدم (try) عشان لو صار خطأ في الكود ما يطفي البرنامج بوجهنا.", 
        "example": "try:\n    res = 10 / 0\nexcept:\n    print('ما تقدر تقسم على صفر!')", 
        "exercise": "جرب تسوي عملية قسمة داخل بلوك try.", 
        "solution": "try:\n    x = 1/0\nexcept:\n    print('Error')"
    }
}

# --- 🏛️ دروس C++ المطورة (شرح روبين) ---
lessons_cpp = {
    "1": {
        "title": "الدرس 1: الهيكل 🏛️", 
        "explanation": "هذا هو العمود الفقري لأي برنامج C++. لازم تبدأ بهذي الرسمة عشان الكمبيوتر يفهم إن هنا يبدأ الشغل وهنا ينتهي. بدونها الكود ضايع!", 
        "example": "#include <iostream>\nusing namespace std;\n\nint main() {\n    return 0;\n}", 
        "exercise": "اكتب الهيكل الأساسي لبرنامج C++.", 
        "solution": "int main() { return 0; }"
    },
    "2": {
        "title": "الدرس 2: الطباعة (cout) 📢", 
        "explanation": "علامة الـ (cout) هي المايكروفون حقك. والأسهم (<<) كأنها تقول للكمبيوتر: 'خذ هالكلام وطلعه برا على الشاشة'.", 
        "example": "cout << 'أهلاً بك في عالم العمالقة';", 
        "exercise": "اطبع اسمك الحين باستخدام cout.", 
        "solution": "cout << 'Osman';"
    },
    "3": {
        "title": "الدرس 3: المتغيرات 📦", 
        "explanation": "في C++ لازم تكون نظامي! تبي تخزن رقم؟ قله (int). تبي حرف؟ قله (char). كأنك تحدد نوع الكرتون قبل ما تحط فيه الغرض.", 
        "example": "int age = 20;\nchar grade = 'A';", 
        "exercise": "عرف متغير رقمي (int) وسوه يساوي 10.", 
        "solution": "int a = 10;"
    },
    "4": {
        "title": "الدرس 4: الإدخال (cin) 📥", 
        "explanation": "عكس الطباعة! هنا الأسهم (>>) تقول للكمبيوتر: 'اسحب المعلومة من المستخدم وحطها داخل الصندوق (المتغير)'.", 
        "example": "int x;\ncin >> x;", 
        "exercise": "اطلب من المستخدم يدخل عمره في متغير باسم age.", 
        "solution": "cin >> age;"
    },
    "5": {
        "title": "الدرس 5: الشروط ⚖️", 
        "explanation": "هنا يبدأ الذكاء! البرنامج يوقف عند إشارة مرور: لو الشارع فاضي (الشرط صح) يمر، ولو زحمة (الشرط خطأ) يروح طريق ثاني.", 
        "example": "if (x > 5) {\n    cout << 'كبير';\n} else {\n    cout << 'صغير';\n}", 
        "exercise": "تحقق لو x تساوي 5، اطبع 'OK'.", 
        "solution": "if (x == 5) { cout << 'OK'; }"
    },
    "6": {
        "title": "الدرس 6: For Loop 🔄", 
        "explanation": "بدل ما تكرر الكود يدوي، عط البرنامج عدد مرات التكرار وخلّه يركض لين يوصل للنهاية اللي حددتها له.", 
        "example": "for(int i=0; i<5; i++) {\n    cout << 'تكرار';\n}", 
        "exercise": "سوي حلقة تكرار تطبع كلمة 'Win' ثلاث مرات.", 
        "solution": "for(int i=0; i<3; i++) { cout << 'Win'; }"
    },
    "7": {
        "title": "الدرس 7: While 🔁", 
        "explanation": "هذي الحلقة تقول للبرنامج: 'دام الشرط لسا صح، خلك شغال ولا توقف'. مثل الغسالة، تدور لين يخلص الوقت!", 
        "example": "while (energy > 0) {\n    cout << 'أعمل..';\n}", 
        "exercise": "سوي while loop يشتغل دام x أصغر من 10.", 
        "solution": "while(x < 10) { }"
    },
    "8": {
        "title": "الدرس 8: المصفوفات (Arrays) 📊", 
        "explanation": "تخيلها كأنها 'عمارة' فيها شقق مرقمة. كل شقة فيها معلومة، بدل ما تسوي 10 بيوت منفصلة، اجمعها في عمارة وحدة!", 
        "example": "int scores[3] = {90, 85, 70};", 
        "exercise": "عرف مصفوفة أرقام تشيل 5 عناصر.", 
        "solution": "int arr[5];"
    },
    "9": {
        "title": "الدرس 9: الدوال 🛠️", 
        "explanation": "بدل ما تكتب كود طويل، سوي 'ورشة عمل' صغيرة (دالة) وسوها مرة وحدة، وكل ما احتجتها بس نادِ اسمها.", 
        "example": "void sayHi() {\n    cout << 'هلا بالذيب';\n}", 
        "exercise": "عرف دالة بسيطة نوعها void واسمها test.", 
        "solution": "void test() { }"
    },
    "10": {
        "title": "الدرس 10: المؤشرات (Pointers) 📍", 
        "explanation": "هذا 'لوكيشن' المعلومة! بدل ما تعطيني الغرض نفسه، عطني عنوانه في ذاكرة الكمبيوتر وين مكانه بالضبط.", 
        "example": "int* p = &x; // p الحين يعرف وين ساكنة x", 
        "exercise": "عرف مؤشر (Pointer) يشير لمتغير باسم a.", 
        "solution": "int* p = &a;"
    },
    "11": {
        "title": "الدرس 11: الكلاسات (Classes) 🏢", 
        "explanation": "هذا 'مخطط المهندس'. ترسم فيه صفات (مثل الطول واللون) وأفعال، وبعدين تستخدم هالمخطط عشان تبني منه أشياء حقيقية.", 
        "example": "class Car {\n    public: string brand;\n};", 
        "exercise": "عرف كلاس بسيط باسم User.", 
        "solution": "class User { };"
    },
    "12": {
        "title": "الدرس 12: الكائنات (Objects) 🤖", 
        "explanation": "تذكر المخطط اللي سويناه في الدرس اللي راح؟ الكائن هو 'المنتج' الفعلي اللي صنعناه من هذا المخطط.", 
        "example": "Car myCar;\nmyCar.brand = 'Toyota';", 
        "exercise": "سوي كائن (Object) من كلاس User واسمه osman.", 
        "solution": "User osman;"
    },
    "13": {
        "title": "الدرس 13: هياكل البيانات (Struct) 🔗", 
        "explanation": "لو تبي تسوي 'بطاقة تعريف' فيها اسمك وعمرك ورقمك مع بعض، الـ struct يجمع لك هالمعلومات المختلفة في باقة وحدة.", 
        "example": "struct Student {\n    int id;\n    string name;\n};", 
        "exercise": "عرف struct بسيط باسم Node.", 
        "solution": "struct Node { };"
    },
    "14": {
        "title": "الدرس 14: لغة الآلة (ASCII) 🔐", 
        "explanation": "الكمبيوتر ما يفهم حروف، يفهم أرقام! كل حرف له رقم سري وراه (مثلاً A هو 65). هنا نتعلم كيف نتلاعب بهذي الأرقام.", 
        "example": "char c = 'A';\nc = c + 1; // صار الحرف B الحين!", 
        "exercise": "شفر حرف z بزيادة 1 عليه (عن طريق ++).", 
        "solution": "z++;"
    }
}

import html # أهم سطر فوق!

def send_lesson(bot, chat_id, lesson_data, n, prefix):
    # الخطوة السحرية: تنظيف كل النصوص من أي علامات < أو >
    title = html.escape(lesson_data['title'])
    explanation = html.escape(lesson_data['explanation'])
    example = html.escape(lesson_data['example'])
    
    # الحين نركب الرسالة بأمان 100%
    msg = (
        f"<b>◈╼╼╼╼╼╼╼╼╼╼╼╼╼╼╼╼◈</b>\n"
        f"<b>{title}</b>\n"
        f"<b>◈╼╼╼╼╼╼╼╼╼╼╼╼╼╼╼╼◈</b>\n\n"
        f"<b>💡 وش السالفة؟ (الشرح):</b>\n"
        f"<i>{explanation}</i>\n\n"
        f"<b>💻 كود للتطبيق:</b>\n"
        f"<code>{example}</code>\n\n"
        f"<b>◈╼╼╼╼╼╼╼╼╼╼╼╼╼╼╼╼◈</b>"
    )
    
    mk = types.InlineKeyboardMarkup()
    mk.add(types.InlineKeyboardButton("🎯 ابدأ التحدي الآن", callback_data=f"{prefix}_ex_{n}"))
    
    try:
        bot.send_message(chat_id, msg, parse_mode="HTML", reply_markup=mk)
    except Exception as e:
        # لو لا قدر الله صار خطأ، يطبع لك وش النص اللي خرب العملية
        print(f"Error in Lesson {n}: {e}")
        bot.send_message(chat_id, "⚠️ عذراً، فيه مشكلة في عرض هذا الدرس، جاري إصلاحها!")


# --- 🐍 بوت بايثون ---
@bot_py.message_handler(commands=['start'])
def py_start(m):
    mk = types.ReplyKeyboardMarkup(resize_keyboard=True).add("🐍 دروس بايثون")
    bot_py.send_message(m.chat.id, "أهلاً بك في Bot Empire بايثون 🐍!", reply_markup=mk)

@bot_py.message_handler(func=lambda m: m.text == "🐍 دروس بايثون")
def py_list(m):
    mk = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    btns = [types.KeyboardButton(f"بايثون {i}") for i in range(1, 13)]
    mk.add(*btns)
    bot_py.send_message(m.chat.id, "اختر الدرس:", reply_markup=mk)

@bot_py.message_handler(func=lambda m: m.text and m.text.startswith("بايثون "))
def py_h(m):
    n = m.text.split()[1]
    if n in lessons_py: send_lesson(bot_py, m.chat.id, lessons_py[n], n, "py")

@bot_py.callback_query_handler(func=lambda c: c.data.startswith("py_"))
def py_c(c):
    _, act, n = c.data.split("_")
    if act == "ex":
        mk = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("🔑 الحل", callback_data=f"py_sol_{n}"))
        bot_py.edit_message_text(f"🎯 التحدي: {lessons_py[n]['exercise']}", c.message.chat.id, c.message.message_id, reply_markup=mk)
    elif act == "sol":
        bot_py.edit_message_text(f"✅ الحل: <code>{lessons_py[n]['solution']}</code>", c.message.chat.id, c.message.message_id, parse_mode="HTML")

# --- 🦾 بوت C++ ---
@bot_cpp.message_handler(commands=['start'])
def cpp_start(m):
    mk = types.ReplyKeyboardMarkup(resize_keyboard=True).add("🦾 دروس C++")
    bot_cpp.send_message(m.chat.id, "أهلاً بك في Bot Empire C++ 🦾!", reply_markup=mk)

@bot_cpp.message_handler(func=lambda m: m.text == "🦾 دروس C++")
def cpp_list(m):
    mk = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    btns = [types.KeyboardButton(f"درس {i}") for i in range(1, 15)]
    mk.add(*btns)
    bot_cpp.send_message(m.chat.id, "اختر الدرس:", reply_markup=mk)

@bot_cpp.message_handler(func=lambda m: m.text and m.text.startswith("درس "))
def cpp_h(m):
    n = m.text.split()[1]
    if n in lessons_cpp: send_lesson(bot_cpp, m.chat.id, lessons_cpp[n], n, "cp")

@bot_cpp.callback_query_handler(func=lambda c: c.data.startswith("cp_"))
def cpp_c(c):
    _, act, n = c.data.split("_")
    if act == "ex":
        mk = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("🔑 الحل", callback_data=f"cp_sol_{n}"))
        bot_cpp.edit_message_text(f"🎯 التحدي: {lessons_cpp[n]['exercise']}", c.message.chat.id, c.message.message_id, reply_markup=mk)
    elif act == "sol":
        bot_cpp.edit_message_text(f"✅ الحل: <code>{lessons_cpp[n]['solution']}</code>", c.message.chat.id, c.message.message_id, parse_mode="HTML")

# --- 🤖 بوت لاري (AI) ---
@bot_ai.message_handler(commands=['start'])
def ai_start(m):
    save_user(m)
    mk = types.InlineKeyboardMarkup(row_width=1).add(
        types.InlineKeyboardButton("👨‍🏫 وضع المدرس", callback_data="set_teacher"),
        types.InlineKeyboardButton("💀 نمط الهكر", callback_data="set_hacker"),
        types.InlineKeyboardButton("🤝 وضع الصديق", callback_data="set_friend")
    )
    bot_ai.send_message(m.chat.id, "مرحباً! أنا لاري مساعدك الذكي. اختر شخصيتي التي تريدني اتعمامل معك بها \n بعض الناس يختارون الهكر ولكنك قد تكون مختلف عنهم :", reply_markup=mk)

@bot_ai.message_handler(commands=['settings'])
def ai_settings(m):
    mk = types.InlineKeyboardMarkup(row_width=1).add(
        types.InlineKeyboardButton("👨‍🏫 وضع المدرس", callback_data="set_teacher"),
        types.InlineKeyboardButton("💀 نمط الهكر", callback_data="set_hacker"),
        types.InlineKeyboardButton("🤝 وضع الصديق", callback_data="set_friend")
    )
    bot_ai.send_message(m.chat.id, "يمكنك تغيير الشخصية بسهولة من هنا:", reply_markup=mk)

# --- 🛠️ هذي الدالة اللي تعدلها عشان تختفي الأزرار وتتحدث الرسالة ---
@bot_ai.callback_query_handler(func=lambda c: c.data.startswith("set_"))
def update_persona(c):
    p = c.data.split("_")[1] # نأخذ الجزء اللي بعد الـ set_
    user_modes[c.message.chat.id] = CHARACTERS[p]
    
    # تحويل الاختيار لاسم عربي عشان يطلع بالرسالة
    names = {"teacher": "المدرس 👨‍🏫", "hacker": "الهكر 💀", "friend": "الصديق 🤝"}
    chosen_name = names.get(p, p)
    
    # 1. إظهار تنبيه صغير فوق (Alert)
    bot_ai.answer_callback_query(c.id, f"تم تفعيل وضع {chosen_name}")
    
    # 2. تعديل الرسالة نفسها (بدال إرسال رسالة جديدة)
    bot_ai.edit_message_text(
        chat_id=c.message.chat.id,
        message_id=c.message.message_id,
        text=f"✅ لاري الآن بوضعية: **{chosen_name}**",
        parse_mode="Markdown"
    )

# --- دالة بدء الإذاعة المعدلة ---
@bot_ai.message_handler(func=lambda m: m.text == "اذاعه")
def start_broadcast(m):
    if m.from_user.id == ADMIN_ID: # تأكدنا من الأيدي
        msg = bot_ai.send_message(m.chat.id, "📢 **أهلاً أيها المطور.. اكتب الآن الرسالة التي تريد بثها للجميع:**")
        bot_ai.register_next_step_handler(msg, do_broadcast)
    else:
        bot_ai.reply_to(m, "❌ هذا الأمر مخصص للإمبراطور عثمان فقط!")

# --- دالة التنفيذ النهائية ---
def do_broadcast(m):
    # تنسيق الرسالة بشكل احترافي HTML عشان ما تضرب مع اليوزر
    final_msg = (
        "<b>❰ 📢 رسالة من المطور ❱</b>\n\n"
        "◈—╼—╼—╼—╼—╼—╼—◈\n\n"
        f"{m.text}\n\n" 
        "◈—╼—╼—╼—╼—╼—╼—◈\n\n"
        "💠 <b>Dev:</b> @Xx_Rol"
    )

    try:
        if not os.path.exists(users_file):
            bot_ai.send_message(ADMIN_ID, "❌ ملف المستخدمين غير موجود!")
            return

        with open(users_file, "r", encoding="utf-8") as f:
            users = f.read().splitlines()
        
        users = list(set(users)) # إزالة التكرار لضمان عدم الإزعاج
        count = 0
        
        for user in users:
            if not user.strip(): continue # تخطي الأسطر الفارغة
            try:
                # استخدمنا HTML هنا عشان يوزر @Xx_Rol ما يسبب خطأ
                bot_ai.send_message(user, final_msg, parse_mode="HTML")
                count += 1
                time.sleep(0.05) # تأخير بسيط جداً لتجنب حظر التليجرام (Flood)
            except Exception:
                continue
        
        bot_ai.send_message(ADMIN_ID, f"✅ تم بنجاح! أرسلنا رسالتك لـ {count} بطل.")
    except Exception as e:
        bot_ai.send_message(ADMIN_ID, f"❌ حدث خطأ تقني: {e}")

@bot_ai.message_handler(func=lambda m: True)
def ai_handler(m):
    chat_id = m.chat.id
    current_persona = user_modes.get(chat_id, CHARACTERS["teacher"])
    history = get_history(chat_id)
    messages = [{"role": "system", "content": current_persona}] + history + [{"role": "user", "content": m.text}]
    try:
        resp = client_llama.chat.completions.create(messages=messages, model="llama-3.1-8b-instant")
        reply = resp.choices[0].message.content
        bot_ai.reply_to(m, reply)
        update_memory(chat_id, "user", m.text)
        update_memory(chat_id, "assistant", reply)
    except: bot_ai.reply_to(m, " لاري تعب شوي، جرب لاحقاً.")


# --- 🚀 تشغيل الخيوط ---
def run_bot(bot, name):
    while True:
        try:
            print(f"📡 {name} is running...")
            bot.polling(none_stop=True)
        except: time.sleep(5)

threading.Thread(target=run_bot, args=(bot_py, "Python Bot"), daemon=True).start()
threading.Thread(target=run_bot, args=(bot_cpp, "C++ Bot"), daemon=True).start()
threading.Thread(target=run_bot, args=(bot_ai, "AI Bot"), daemon=True).start()

print("✅ Bot Empire is officially ONLINE!")
while True: time.sleep(10)


