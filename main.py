import telebot
from deep_translator import GoogleTranslator

API_TOKEN = '7611084205:AAF39-vEofFj0A9Z6_jUeGfRAt37B9A-Mms'
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "أهلاً بك! أنا بوت الترجمة المطور. أرسل لي أي نص وسأترجمه فوراً.")

@bot.message_handler(func=lambda message: True)
def translate_message(message):
    try:
        # الترجمة للعربية
        to_ar = GoogleTranslator(source='auto', target='ar').translate(message.text)
        # الترجمة للإنجليزية
        to_en = GoogleTranslator(source='auto', target='en').translate(message.text)
        
        response = f"🇸🇦 **العربية:**\n{to_ar}\n\n🇺🇸 **English:**\n{to_en}"
        bot.reply_to(message, response, parse_mode='Markdown')
    except Exception as e:
        bot.reply_to(message, "عذراً، حدث خطأ أثناء الترجمة.")

print("البوت يعمل الآن بنجاح...")
bot.infinity_polling()
