import telebot
import requests
from bs4 import BeautifulSoup
import datetime
import calendar
from data.testing.web_site_parser import availability_of_tickets

token = open("token.txt", "r")
bot = telebot.TeleBot(token.read())

url = 'https://mosmetro.ru/passengers/information/special-tickets/'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')
tickets_info = soup.find_all('p')

today_date = datetime.date.isoformat(datetime.date.today()).split('-')
today_date.reverse()

loop_list = []

day = 4 -1
month = 11
year = 2021

#day = int(today_date[0]) -1
#month = int(today_date[1])
#year = int(today_date[2])

last_day = calendar.monthrange(year,month)[-1]
week_list = []

@bot.message_handler(commands=['start'])
def start_message(message):
	bot.send_message(message.chat.id,'Вас приветствует Бот Эйситристик, здесь вы сможете узнавать о выходе юбилейных единых билетов в Московском метрополитене. \nЧто бы проверить информацию о билетах на ближайшие 7 дней, напишите команду "Проверить юбилейные билеты" или сокращенно "пюб".')

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "Проверить юбилейные билеты" or message.text == "проверить юбилейные билеты" or message.text == "пюб":
        bot.send_message(message.from_user.id, "Привет, я нашел вот такие юбилейные билеты:")
        bot.send_message(message.chat.id, availability_of_tickets(tickets_info, loop_list, day, month, year, last_day, week_list))
        #bot.send_photo(message.from_user.id, "https://mosmetro.ru/local/assets/imgs/special-tickets/photo_2021-11-01 16.15.34.jpeg") bot.send_photo(id, photo, caption='текст')
    elif message.text == "/help":
        bot.send_message(message.from_user.id, 'Напиши "Проверить юбилейные билеты" или сокращенно "пюб"')
    else:
        bot.send_message(message.from_user.id, "Команда не распознана. Напиши /help.")

bot.polling(none_stop=True, interval=0)
