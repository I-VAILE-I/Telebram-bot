import dataclasses
from typing import List
import bs4
import telebot
import requests
from bs4 import BeautifulSoup
import datetime
from telebot.types import Message

token = open("token.txt", "r")
bot = telebot.TeleBot(token.read())

URL = 'https://mosmetro.ru/passengers/information/special-tickets/'


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, """
    Вас приветствует Бот Эйситристик, здесь вы сможете узнавать о выходе юбилейных единых билетов в
    Московском метрополитене. Что бы проверить информацию о билетах на ближайшие 7 
    дней, напишите команду "Проверить юбилейные билеты" или сокращенно "пюб".
    """)


@dataclasses.dataclass
class Ticket:
    web_tag: bs4.element.Tag
    name: str
    date: datetime


# tickets_all_on_page[0].web_tag.find_next('img').get('src') - для картинок

def convert_str_to_date(date_time_str: str) -> datetime:
    return datetime.datetime.strptime(date_time_str, '%d.%m.%Y')


def get_date_from_ticket_text(text: str) -> str:
    start_index = text.find('(') + 1
    end_index = start_index + 10
    return text[start_index:end_index]


def get_name_from_ticket_text(text: str) -> str:
    start_index = text.find('«') + 1
    end_index = text.find('»') - 1
    return text[start_index:end_index]


def get_all_tickets_on_page(url: str) -> List[Ticket]:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    tickets_info = soup.find_all('p')
    tickets: List[Ticket] = []
    for ticket in tickets_info:
        if 'Билет' in ticket.text:
            tickets.append(
                Ticket(
                    web_tag=ticket.text,
                    name=get_name_from_ticket_text(ticket.text),
                    date=convert_str_to_date(
                        get_date_from_ticket_text(ticket.text)
                    )
                )
            )
    return tickets


tickets = get_all_tickets_on_page(url=URL)
# start = datetime.datetime.today() - datetime.timedelta(days=1) #для правильной работы
start = convert_str_to_date('10.11.2020') - datetime.timedelta(days=1) #для проверки и отладки мнодественного вывода билетов
end = start + datetime.timedelta(days=7)


def get_tickets_by_date(
        tickets: List[Ticket],
        start: datetime.datetime,
        end: datetime.datetime,
    ) -> List[Ticket]:
    l = []
    for d in tickets:
        if d.date >= start:
            if d.date <= end:
                l.append(d)
    return l


url_photo = 'https://mosmetro.ru/passengers/information/special-tickets/'
photo_response = requests.get(url_photo)
photo_soup = BeautifulSoup(photo_response.text, 'lxml')
photo_url = photo_soup.find_all(width="333")
tickets_info = photo_soup.find_all('p')

tickets_on_week: List[Ticket] = get_tickets_by_date(tickets=tickets, start=start, end=end)
amount = len(tickets_on_week)

only_tickets = []
for tickets_info in tickets_info:
    if 'Билет' in tickets_info.text:
        only_tickets.append(tickets_info.text)


def tickets_photos(
        photo_url,
        amount,
        only_tickets
    ):
    img_url = []
    photo = []
    id_photo = []
    using_id = 0
    for i in range(amount * 2):
        for id in range(amount):
            if using_id != amount:
                id_photo.append(only_tickets.index(tickets_on_week[id].web_tag) * 2)
                id_photo.append(only_tickets.index(tickets_on_week[id].web_tag) * 2 + 1)
                using_id += 1
            else:
                break
        otriv = 0
        rashodnik = str(photo_url[id_photo[i]]) + '"'
        rashodnik.split('"')
        for j in range(len(rashodnik)):
            if rashodnik[j] == '"' and otriv != 1:
                znach = True
                otriv += 1
                inde_X = j + 1
                while znach == True:
                    img_url.append(rashodnik[inde_X])
                    inde_X += 1
                    if rashodnik[inde_X] == '"':
                        znach = False
                photo_url_ = 'https://mosmetro.ru' + ''.join(img_url)
                photo.append(photo_url_)
                img_url.clear()
    return photo


photo_list = tickets_photos(photo_url, amount, only_tickets)


@bot.message_handler(content_types=['text'])
def get_text_messages(message: Message):
    if message.text == "Проверить юбилейные билеты" or message.text == "проверить юбилейные билеты" or message.text == "пюб" or message.text == "Пюб":
        # tickets_all_on_page: List[Ticket] = get_all_tickets_on_page(url=URL)
        tickets_on_week: List[Ticket] = get_tickets_by_date(tickets=tickets, start=start, end=end)
        if len(tickets_on_week) != 0:
            bot.send_message(message.from_user.id, "Привет, я нашел вот такие юбилейные билеты:")
            id = -1
            for i in range(len(tickets_on_week)):
                ticket_name = 'Юбилейный билет в честь:' + ' ' + tickets_on_week[i].name
                ticket_date = 'Ищите в кассах метрополитена в:' + ' ' + tickets_on_week[i].date.strftime('%d.%m.%Y')
                for j in range(1):
                    bot.send_message(message.from_user.id, ticket_name)
                    id += 1
                    bot.send_photo(message.from_user.id, photo_list[id], caption=ticket_date)
                    id += 1
                    bot.send_photo(message.from_user.id, photo_list[id], caption=ticket_date)
        else:
            bot.send_message(message.from_user.id, "Привет, на ближайшие 7 дней никаких юбилейных билетов не обнаружено. :(")

    elif message.text == "/help":
        bot.send_message(message.from_user.id, 'Напишите "Проверить юбилейные билеты" или сокращенно "пюб"')
    else:
        bot.send_message(message.from_user.id, "Команда не распознана. Напишите /help.")


bot.polling(none_stop=True, interval=0)
