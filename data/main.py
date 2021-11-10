import telebot
import requests
from bs4 import BeautifulSoup
import datetime
import calendar
from data.testing.web_site_parser import availability_of_tickets
from data.testing.geting_photo_url import tickets_photos

token = open("token.txt", "r")
bot = telebot.TeleBot(token.read())

url = 'https://mosmetro.ru/passengers/information/special-tickets/'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')
tickets_info = soup.find_all('p')

today_date = datetime.date.isoformat(datetime.date.today()).split('-')
today_date.reverse()

loop_list = []

# day = 4 -1
# month = 11
# year = 2021

day = int(today_date[0]) -1
month = int(today_date[1])
year = int(today_date[2])

last_day = calendar.monthrange(year,month)[-1]
week_list = []

url = 'https://mosmetro.ru/passengers/information/special-tickets/'
photo_response = requests.get(url)
photo_soup = BeautifulSoup(photo_response.text, 'lxml')
photo_url = photo_soup.find_all(width="333")

img_url = []
photo = []
znach = False
otriv = 0
kolvo = 1 * 2

itog_date = availability_of_tickets(tickets_info, loop_list, day, month, year, last_day, week_list)
itog_photo = tickets_photos(photo_url, otriv, kolvo, znach, photo, img_url)

@bot.message_handler(commands=['start'])
def start_message(message):
	bot.send_message(message.chat.id,'Вас приветствует Бот Эйситристик, здесь вы сможете узнавать о выходе юбилейных единых билетов в Московском метрополитене. \nЧто бы проверить информацию о билетах на ближайшие 7 дней, напишите команду "Проверить юбилейные билеты" или сокращенно "пюб".')

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "Проверить юбилейные билеты" or message.text == "проверить юбилейные билеты" or message.text == "пюб":
        bot.send_message(message.from_user.id, "Привет, я нашел вот такие юбилейные билеты:")
        bot.send_message(message.chat.id, itog_date)
        for i in range(len(itog_photo)):
            bot.send_photo(message.from_user.id, itog_photo[i], "Их внешний вид.") #bot.send_photo(id, photo, caption='текст')
    elif message.text == "/help":
        bot.send_message(message.from_user.id, 'Напишите "Проверить юбилейные билеты" или сокращенно "пюб"')
    else:
        bot.send_message(message.from_user.id, "Команда не распознана. Напишите /help.")

bot.polling(none_stop=True, interval=0)
