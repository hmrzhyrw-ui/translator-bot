import telebot
from telebot import types
from googletrans import Translator
from gtts import gTTS
import os

# --- الإعدادات ---
TOKEN = '8663782040:AAGLGVOKaupHt_zMAeWf-CuMShHoq0QF1z0'
bot = telebot.TeleBot(TOKEN)
translator = Translator()

# تخزين اختيار اللغة لكل مستخدم (مؤقتاً)
user_lang = {}

# --- قائمة اللغات المتاحة ---
LANGUAGES = {
    'ar': 'العربية 🇸🇦',
    'en': 'الإنجليزية 🇺🇸',
    'fr': 'الفرنسية 🇫🇷',
    'tr': 'التركية 🇹🇷',
    'es': 'الإسبانية 🇪🇸',
    'de': 'الألمانية 🇩🇪'
}

# --- رسالة الترحيب واختيار اللغة ---
@bot.message_handler(commands=['start', 'help', 'setlang'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    buttons = [types.InlineKeyboardButton(text=name, callback_data=code) for code, name in LANGUAGES.items()]
    markup.add(*buttons)
    
    bot.reply_to(message, "🌍 أهلاً بك! اختر اللغة التي تريد الترجمة إليها أولاً:", reply_markup=markup)

# --- معالجة اختيار اللغة من الأزرار ---
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data in LANGUAGES:
        user_lang[call.message.chat.id] = call.data
        bot.answer_callback_query(call.id, f"تم اختيار {LANGUAGES[call.data]}")
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, 
                              text=f"✅ ممتاز! سأترجم الآن أي نص ترسلُه إلى **{LANGUAGES[call.data]}**.")

# --- معالجة النصوص والترجمة ---
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    chat_id = message.chat.id
    
    # التأكد من أن المستخدم اختار لغة، وإلا فالعربية هي الافتراضية
    target_lang = user_lang.get(chat_id, 'ar')
    
    try:
        bot.send_chat_action(chat_id, 'typing')
        
        # الترجمة إلى اللغة المختارة
        translation = translator.translate(message.text, dest=target_lang)
        translated_text = translation.text
        
        # إرسال النص المترجم
        bot.reply_to(message, f"💬 **الترجمة ({LANGUAGES[target_lang]}):**\n\n`{translated_text}`", parse_mode='Markdown')

        # تحويل الترجمة لصوت (إذا كانت اللغة مدعومة في gTTS)
        try:
            bot.send_chat_action(chat_id, 'record_audio')
            tts = gTTS(text=translated_text, lang=target_lang)
            audio_file = f"voice_{chat_id}.mp3"
            tts.save(audio_file)

            with open(audio_file, 'rb') as audio:
                bot.send_voice(chat_id, audio, caption=f"🔊 نطق الترجمة ({LANGUAGES[target_lang]})")
            os.remove(audio_file)
        except:
            pass # بعض اللغات قد لا تدعم النطق الصوتي

    except Exception as e:
        bot.reply_to(message, "❌ حدث خطأ، يرجى المحاولة لاحقاً.")

# --- تشغيل ---
print("🚀 بوت الترجمة المتعددة يعمل الآن...")
bot.infinity_polling()
