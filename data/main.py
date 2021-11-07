import telebot

bot = telebot.TeleBot('2062309923:AAExMItj8JzG6w_ybDm0dquLHPeEiwCVbZQ')
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "Проверить юбилейные билеты" \
    or message.text == "проверить юбилейные билеты" \
    or message.text == "пюб":
        if tickets == True:
            bot.send_message(message.from_user.id, "Привет, я нашел вот такие юбилейные билеты")
        else:
            bot.send_message(message.from_user.id, "Привет, я нашел вот такие юбилейные билеты")
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "Напиши")
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")

tickets = True

bot.polling(none_stop=True, interval=0)
