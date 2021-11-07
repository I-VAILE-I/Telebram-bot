import telebot

token = open("token.txt", "r")
bot = telebot.TeleBot(token.read())

@bot.message_handler(commands=['start'])
def start_message(message):
	bot.send_message(message.chat.id,'Вас приветствует Бот Эйситристик, здесь вы сможете узнавать о выходе юбилейных единых билетов в Московском метрополитене. \nЧто бы проверить информацию о билетах на ближайшие 7 дней, напишите команду "Проверить юбилейные билеты" или сокращенно "пюб".')

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "Проверить юбилейные билеты" or message.text == "проверить юбилейные билеты" or message.text == "пюб":
        bot.send_message(message.from_user.id, "Привет, я нашел вот такие юбилейные билеты:")
    elif message.text == "/help":
        bot.send_message(message.from_user.id, 'Напиши "Проверить юбилейные билеты" или сокращенно "пюб"')
    else:
        bot.send_message(message.from_user.id, "Команда не распознана. Напиши /help.")

bot.polling(none_stop=True, interval=0)
