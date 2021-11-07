import telebot
token = open("token.txt", "r")
bot = telebot.TeleBot(token.read())
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "Проверить юбилейные билеты" or message.text == "проверить юбилейные билеты" or message.text == "пюб":
        bot.send_message(message.from_user.id, "Привет, я нашел вот такие юбилейные билеты")
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "Напиши")
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")

bot.polling(none_stop=True, interval=0)
