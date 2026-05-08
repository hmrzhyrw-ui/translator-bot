import telebot
from deep_translator import GoogleTranslator

# الرمز الجديد الذي أرسلته
API_TOKEN = '8114421183:AAHeuO2K3xX9P78m5D982N0S98W8S8W8S8W'
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "أهلاً بك في بوت الترجمة! 💬\nأرسل لي أي نص وسأقوم بترجمته فوراً للعربية والإنجليزية.")

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
        bot.reply_to(message, "عذراً، حدث خطأ أثناء الترجمة. حاول مرة أخرى.")

print("البوت بدأ العمل بالرمز الجديد...")
bot.infinity_polling()
