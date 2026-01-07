import os, telebot, threading, http.server, socketserver, time, html
from telebot import types

# جلب التوكنات من Koyeb
TOKEN_PY = os.getenv("TELEGRAM_TOKEN")   
TOKEN_CPP = os.getenv("TELEGRAM_TOKEN2") 

bot_py = telebot.TeleBot(TOKEN_PY)
bot_cpp = telebot.TeleBot(TOKEN_CPP)

# --- 🐍 دروس بايثون الوافية (12 درس) ---
lessons_py = {
    "1": {"title": "الدرس 1: الطباعة (print) 🐍", "explanation": "تعتبر دالة print هي أول خطوة لتعلم أي لغة، ووظيفتها عرض النصوص والنتائج للمستخدم على الشاشة.", "example": "print('مرحباً بك في عالم بايثون')", "exercise": "اطبع اسمك الثلاثي باستخدام دالة print.", "solution": "print('عثمان ... ...')"},
    "2": {"title": "الدرس 2: المتغيرات (Variables) 📦", "explanation": "المتغيرات هي مخازن في الذاكرة نحفظ فيها البيانات (أرقام أو نصوص) لنستخدمها لاحقاً في الكود.", "example": "name = 'Osman'\nage = 20", "exercise": "عرف متغير باسم country وضع فيه اسم بلدك.", "solution": "country = 'Saudi Arabia'"},
    "3": {"title": "الدرس 3: العمليات الحسابية ➗", "explanation": "بايثون بارعة في الحساب! يمكنك الجمع (+)، الطرح (-)، الضرب (*)، والقسمة (/).", "example": "x = 10 + 5 * 2", "exercise": "احسب حاصل ضرب 5 في 5 واطبعه.", "solution": "print(5 * 5)"},
    "4": {"title": "الدرس 4: الإدخال (input) 📥", "explanation": "دالة input تسمح للبرنامج بالتفاعل مع المستخدم وأخذ معلومات منه أثناء تشغيل الكود.", "example": "user_name = input('ما هو اسمك؟ ')", "exercise": "اطلب من المستخدم إدخال عمره وخزنه في متغير.", "solution": "age = input('كم عمرك؟ ')"},
    "5": {"title": "الدرس 5: القوائم (Lists) 📚", "explanation": "القائمة هي متغير واحد يمكنه تخزين الكثير من القيم بترتيب معين، ونستخدم الأقواس المربعة [].", "example": "fruits = ['تفاح', 'موز', 'برتقال']", "exercise": "أنشئ قائمة تحتوي على ثلاثة أرقام من اختيارك.", "solution": "nums = [10, 20, 30]"},
    "6": {"title": "الدرس 6: القواميس (Dictionaries) 📖", "explanation": "القاموس يخزن البيانات بنظام (مفتاح وقيمة)، مثل دليل الهاتف (الاسم: الرقم).", "example": "car = {'brand': 'Toyota', 'year': 2024}", "exercise": "أنشئ قاموساً يحتوي على مفتاح 'city' وقيمة 'Riyadh'.", "solution": "d = {'city': 'Riyadh'}"},
    "7": {"title": "الدرس 7: الشروط (if statement) ⚖️", "explanation": "تستخدم لاتخاذ القرارات؛ إذا تحقق الشرط ينفذ الكود، وإذا لم يتحقق ينتقل لغيره.", "example": "if score >= 50:\n    print('ناجح')", "exercise": "اكتب شرطاً يطبع 'موجب' إذا كان الرقم x أكبر من 0.", "solution": "if x > 0:\n    print('موجب')"},
    "8": {"title": "الدرس 8: التكرار (for loop) 🔄", "explanation": "تستخدم لتكرار تنفيذ كود معين لعدد محدد من المرات أو للمرور على عناصر قائمة.", "example": "for i in range(5):\n    print('أنا أتعلم بايثون')", "exercise": "اطبع الأرقام من 0 إلى 2 باستخدام for.", "solution": "for i in range(3):\n    print(i)"},
    "9": {"title": "الدرس 9: الدوال (Functions) ⚙️", "explanation": "الدالة هي كتلة من الكود يتم تعريفها مرة واحدة واستدعاؤها كلما احتجنا إليها لتنظيم العمل.", "example": "def say_hi():\n    print('مرحباً')", "exercise": "عرف دالة باسم welcome تطبع رسالة ترحيبية.", "solution": "def welcome():\n    print('Welcome!')"},
    "10": {"title": "الدرس 10: معالجة الأخطاء (try/except) 🛡️", "explanation": "تستخدم لحماية البرنامج من التوقف المفاجئ في حال حدوث خطأ غير متوقع.", "example": "try:\n    print(10/0)\nexcept:\n    print('خطأ في القسمة')", "exercise": "استخدم try لتجنب انهيار الكود عند تقسيم رقم على صفر.", "solution": "try: 1/0\nexcept: pass"},
    "11": {"title": "الدرس 11: الملفات (Files) 📂", "explanation": "تمكنك بايثون من إنشاء ملفات نصية، القراءة منها، والكتابة عليها برمجياً.", "example": "with open('note.txt', 'w') as f:\n    f.write('Hello')", "exercise": "افتح ملفاً باسم 'test.txt' في وضع القراءة 'r'.", "solution": "open('test.txt', 'r')"},
    "12": {"title": "الدرس 12: المكتبات (Modules) 📦", "explanation": "يمكنك استيراد أكواد جاهزة كتبها مبرمجون آخرون لتوفير الوقت، مثل مكتبة math أو time.", "example": "import math\nprint(math.pi)", "exercise": "استورد مكتبة random.", "solution": "import random"}
}

# --- 🦾 دروس C++ الاحترافية (14 درس) ---
lessons_cpp = {
    "1": {"title": "🏛️ الدرس 1: الهيكل الأساسي", "explanation": "كل برنامج C++ يجب أن يبدأ بتضمين المكتبات ودالة main التي يبدأ من عندها التنفيذ.", "example": "#include <iostream>\nusing namespace std;\nint main() {\n    return 0;\n}", "exercise": "اكتب هيكل دالة main البسيط.", "solution": "int main() { }"},
    "2": {"title": "📥 الدرس 2: الطباعة (cout)", "explanation": "نستخدم cout متبوعة بـ << لطباعة النصوص على الشاشة، ولا ننسى الفاصلة المنقوطة ;", "example": "cout << \"Hello C++\";", "exercise": "اطبع جملة 'I Love C++'.", "solution": "cout << \"I Love C++\";"},
    "3": {"title": "📦 الدرس 3: أنواع البيانات", "explanation": "يجب تحديد نوع المتغير في C++: int للأرقام، double للكسور، و string للنصوص.", "example": "int age = 25;\nstring name = \"Osman\";", "exercise": "عرف متغيراً من نوع double باسم price.", "solution": "double price = 10.5;"},
    "4": {"title": "➗ الدرس 4: العمليات الحسابية", "explanation": "تستخدم نفس الرموز الرياضية المعروفة، ولكن يجب الحذر عند قسمة الأرقام الصحيحة.", "example": "int result = (10 + 2) * 3;", "exercise": "احسب 100 تقسيم 4 وخزنها في متغير.", "solution": "int x = 100 / 4;"},
    "5": {"title": "⚖️ الدرس 5: الجمل الشرطية", "explanation": "تستخدم if و else لتحديد مسار البرنامج بناءً على قيم المتغيرات.", "example": "if(x > 10) {\n    cout << \"Big\";\n}", "exercise": "اكتب شرطاً يتأكد إذا كان x يساوي 5.", "solution": "if(x == 5) { }"},
    "6": {"title": "🔄 الدرس 6: الحلقات (Loops)", "explanation": "حلقة for تستخدم للتكرار بدقة، وتتكون من البداية، الشرط، ومقدار الزيادة.", "example": "for(int i=0; i<5; i++) {\n    cout << i;\n}", "exercise": "كرر عملية الطباعة 10 مرات باستخدام for.", "solution": "for(int i=0; i<10; i++) { }"},
    "7": {"title": "📊 الدرس 7: المصفوفات (Arrays)", "explanation": "تسمح بتخزين مجموعة من العناصر من نفس النوع في متغير واحد بحجم ثابت.", "example": "int grades[5] = {90, 85, 80, 70, 60};", "exercise": "عرف مصفوفة أرقام صحيحة حجمها 10.", "solution": "int arr[10];"},
    "8": {"title": "🔤 الدرس 8: النصوص (Strings)", "explanation": "للتعامل مع النصوص بشكل متقدم نستخدم مكتبة <string> التي توفر مميزات كثيرة.", "example": "#include <string>\nstring text = \"C++ Power\";", "exercise": "عرف متغير نصي باسم message.", "solution": "string message;"},
    "9": {"title": "⚙️ الدرس 9: الدوال (Functions)", "explanation": "الدوال تساعدك في تنظيم كودك؛ نعرف النوع (مثل void) ثم الاسم ثم الأقواس.", "example": "void greet() {\n    cout << \"Hi\";\n}", "exercise": "عرف دالة باسم run لا تعيد أي قيمة.", "solution": "void run() { }"},
    "10": {"title": "🎯 الدرس 10: المؤشرات (Pointers)", "explanation": "المؤشر هو متغير 'ذكي' لا يحفظ رقماً عادياً، بل يحفظ عنوان متغير آخر في الذاكرة.", "example": "int x = 10;\nint* ptr = &x;", "exercise": "عرف مؤشر ptr يشير إلى نوع int.", "solution": "int* ptr;"},
    "11": {"title": "🔗 الدرس 11: المراجع (References)", "explanation": "المرجع هو اسم مستعار لمتغير موجود بالفعل، أي تغيير في المرجع يغير الأصل.", "example": "int x = 5;\nint &ref = x;", "exercise": "عرف مرجعاً باسم r للمتغير count.", "solution": "int &r = count;"},
    "12": {"title": "🧠 الدرس 12: الذاكرة الديناميكية", "explanation": "نستخدم الكلمة المحجوزة new لحجز مساحة في الذاكرة أثناء تشغيل البرنامج.", "example": "int* p = new int;\n*p = 100;", "exercise": "احجز مساحة لنوع double باستخدام new.", "solution": "new double;"},
    "13": {"title": "🏗️ الدرس 13: الهياكل (Structs)", "explanation": "الـ Struct يسمح لك بإنشاء نوع بيانات خاص بك يجمع أنواعاً مختلفة بداخله.", "example": "struct Player {\n    int id;\n    string name;\n};", "exercise": "عرف struct بسيط باسم Book.", "solution": "struct Book { };"},
    "14": {"title": "💎 الدرس 14: الأصناف (Classes)", "explanation": "هي أساس البرمجة كائنية التوجه، حيث تجمع البيانات والوظائف في 'كائن' واحد.", "example": "class Car {\n  public:\n    void drive() { }\n};", "exercise": "عرف كلاس باسم Robot يحتوي على قسم public.", "solution": "class Robot { public: };"}
}

# --- وظائف الإرسال الآمنة (حل مشكلة Error 400) ---
def send_lesson(bot, chat_id, lesson_data, n, prefix):
    # استخدام html.escape لتحويل رموز < > إلى نصوص آمنة لتلجرام
    safe_title = html.escape(lesson_data['title'])
    safe_expl = html.escape(lesson_data['explanation'])
    safe_exam = html.escape(lesson_data['example'])
    
    msg_text = f"<b>{safe_title}</b>\n\n{safe_expl}\n\n💻 <b>مثال توضيحي:</b>\n<code>{safe_exam}</code>"
    
    mk = types.InlineKeyboardMarkup().add(
        types.InlineKeyboardButton("🎯 التحدي", callback_data=f"{prefix}ex_{n}")
    )
    bot.send_message(chat_id, msg_text, parse_mode="HTML", reply_markup=mk)

# --- معالجات بايثون ---
@bot_py.message_handler(commands=['start'])
def py_start(m):
    mk = types.ReplyKeyboardMarkup(resize_keyboard=True).add("🐍 دروس بايثون")
    bot_py.send_message(m.chat.id, "مرحباً بك في بوت تعليم بايثون! اضغط على الزر للبدء.", reply_markup=mk)

@bot_py.message_handler(func=lambda m: m.text == "🐍 دروس بايثون")
def py_list(m):
    mk = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    btns = [types.KeyboardButton(f"بايثون {i}") for i in range(1, 13)]
    mk.add(*btns)
    bot_py.send_message(m.chat.id, "اختر الدرس الذي ترغب في تعلمه الآن:", reply_markup=mk)

@bot_py.message_handler(func=lambda m: m.text.startswith("بايثون "))
def py_handler(m):
    n = m.text.split()[1]
    if n in lessons_py:
        send_lesson(bot_py, m.chat.id, lessons_py[n], n, "py")

@bot_py.callback_query_handler(func=lambda c: c.data.startswith("py"))
def py_callback(c):
    act, n = c.data.split("_")
    l = lessons_py[n]
    if act == "pyex":
        mk = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("🔑 إظهار الحل", callback_data=f"pysol_{n}"))
        bot_py.edit_message_text(f"🎯 <b>التحدي:</b>\n{html.escape(l['exercise'])}", c.message.chat.id, c.message.message_id, parse_mode="HTML", reply_markup=mk)
    else:
        bot_py.edit_message_text(f"✅ <b>الحل النموذجي:</b>\n<code>{html.escape(l['solution'])}</code>", c.message.chat.id, c.message.message_id, parse_mode="HTML")

# --- معالجات C++ ---
@bot_cpp.message_handler(commands=['start'])
def cpp_start(m):
    mk = types.ReplyKeyboardMarkup(resize_keyboard=True).add("🦾 دروس C++")
    bot_cpp.send_message(m.chat.id, "مرحباً بك في بوت تعليم C++ الاحترافي! اضغط على الزر للبدء.", reply_markup=mk)

@bot_cpp.message_handler(func=lambda m: m.text == "🦾 دروس C++")
def cpp_list(m):
    mk = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    btns = [types.KeyboardButton(f"الدرس {i}") for i in range(1, 15)]
    mk.add(*btns)
    bot_cpp.send_message(m.chat.id, "اختر الدرس الذي ترغب في تعلمه الآن:", reply_markup=mk)

@bot_cpp.message_handler(func=lambda m: m.text.startswith("الدرس "))
def cpp_handler(m):
    n = m.text.split()[1]
    if n in lessons_cpp:
        send_lesson(bot_cpp, m.chat.id, lessons_cpp[n], n, "cp")

@bot_cpp.callback_query_handler(func=lambda c: c.data.startswith("cp"))
def cpp_callback(c):
    act, n = c.data.split("_")
    l = lessons_cpp[n]
    if act == "cpex":
        mk = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("🔑 إظهار الحل", callback_data=f"cpsol_{n}"))
        bot_cpp.edit_message_text(f"🎯 <b>التحدي:</b>\n{html.escape(l['exercise'])}", c.message.chat.id, c.message.message_id, parse_mode="HTML", reply_markup=mk)
    else:
        bot_cpp.edit_message_text(f"✅ <b>الحل النموذجي:</b>\n<code>{html.escape(l['solution'])}</code>", c.message.chat.id, c.message.message_id, parse_mode="HTML")

# --- نظام التشغيل ---
def start_polling(bot, name):
    while True:
        try:
            bot.remove_webhook()
            bot.infinity_polling(skip_pending=True)
        except: time.sleep(10)

if __name__ == "__main__":
    threading.Thread(target=lambda: socketserver.TCPServer(("", 8000), http.server.SimpleHTTPRequestHandler).serve_forever(), daemon=True).start()
    threading.Thread(target=start_polling, args=(bot_py, "Python"), daemon=True).start()
    print("🚀 All Bots are running perfectly!")
    start_polling(bot_cpp, "C++")
