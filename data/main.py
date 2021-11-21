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
    images: str = dataclasses.field(default_factory=list)


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


def get_images(text: str) -> str:
    start_index = text.find('=') + 2
    end_index = text.find('.jpeg')
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
                    web_tag=ticket,
                    name=get_name_from_ticket_text(ticket.text),
                    date=convert_str_to_date(
                        get_date_from_ticket_text(ticket.text)
                    ),
                    images=get_images(ticket.text)
                )
            )
    return tickets


tickets = get_all_tickets_on_page(url=URL)
start = convert_str_to_date('11.11.2020') - datetime.timedelta(days=1)
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


@bot.message_handler(content_types=['text'])
def get_text_messages(message: Message):
    if message.text == "Проверить юбилейные билеты" or message.text == "проверить юбилейные билеты" or message.text == "пюб":
        tickets_all_on_page: List[Ticket] = get_all_tickets_on_page(url=URL)
        tickets_on_week: List[Ticket] = get_tickets_by_date(tickets=tickets, start=start, end=end)
        bot.send_message(message.from_user.id, "Привет, я нашел вот такие юбилейные билеты:")
        for i in range(len(tickets_on_week)):
            ticket_name = tickets_on_week[i].name
            ticket_date = tickets_on_week[i].date
            bot.send_message(message.from_user.id, ticket_name, ticket_date.strftime('%d.%m.%Y'))
            bot.send_message(message.from_user.id, tickets_all_on_page[0].web_tag.find_next('img').get('src'))

    elif message.text == "/help":
        bot.send_message(message.from_user.id, 'Напишите "Проверить юбилейные билеты" или сокращенно "пюб"')
    else:
        bot.send_message(message.from_user.id, "Команда не распознана. Напишите /help.")


bot.polling(none_stop=True, interval=0)
