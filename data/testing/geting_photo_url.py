import datetime
import calendar
import requests
from bs4 import BeautifulSoup
from data.testing.web_site_parser import availability_of_tickets

def tickets_photos(photo_url, otriv, kolvo, znach, photo, img_url):
    for i in range(kolvo):
        otriv = 0
        rashodnik = str(photo_url[i]) + '"'
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

url = 'https://mosmetro.ru/passengers/information/special-tickets/'
photo_response = requests.get(url)
photo_soup = BeautifulSoup(photo_response.text, 'lxml')
photo_url = photo_soup.find_all(width="333")



url = 'https://mosmetro.ru/passengers/information/special-tickets/'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')
tickets_info = soup.find_all('p')
tickets_copied = tickets_info
today_date = datetime.date.isoformat(datetime.date.today()).split('-')
today_date.reverse()

only_tickets = []
for tickets_copied in tickets_copied:
    if 'Билет' in tickets_copied.text:
        only_tickets.append(tickets_copied.text)

# print(only_tickets[12])

loop_list = []

name_tickets = []
day = 11 -1
month = 11
year = 2020
#
# #day = int(today_date[0]) -1
# #month = int(today_date[1])
# #year = int(today_date[2])

last_day = calendar.monthrange(year,month)[-1]
week_list = []
print(availability_of_tickets(tickets_info, loop_list, day, month, year, last_day, week_list, name_tickets))
# itog_tickets = availability_of_tickets(tickets_info, loop_list, day, month, year, last_day, week_list, name_tickets)
itog_tickets = ['Билет «Доноры надежды» (16.11.2020)', 'Билет «10 лет новой схеме метро» (14.11.2020)', 'Билет «День качества» (12.11.2020)', 'Билет «ВХУТЕМАС 100» (11.11.2020)']


img_url = []
photo = []
znach = False
znach2 = 0
otriv = 0
kolvo = len(itog_tickets) *2 # 1 text about ticket = 2 tickets photo
id_photo = []
used_ide = []
# print(itog_tickets, len(itog_tickets))
# for id in range(len(itog_tickets)):
#     id_photo.append(only_tickets.index(str(itog_tickets[id]))-1)
# print(id_photo)
using_id = 0
print(availability_of_tickets(tickets_info, loop_list, day, month, year, last_day, week_list, name_tickets))
for i in range(len(itog_tickets)*2):
    for id in range(len(itog_tickets)):
        if using_id != len(itog_tickets):
            id_photo.append(only_tickets.index(str(itog_tickets[id]))*2)
            id_photo.append(only_tickets.index(str(itog_tickets[id]))*2+1)
            using_id += 1
        else:
            break
    otriv = 0
    print(id_photo)
    rashodnik = str(photo_url[id_photo[i]]) + '"'
    print(i, rashodnik)
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

print(photo)

# tickets_photos(photo_url, otriv, kolvo, znach, photo, img_url)