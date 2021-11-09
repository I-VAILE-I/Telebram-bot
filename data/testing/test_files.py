import requests
from bs4 import BeautifulSoup
import datetime
import calendar

#def availability_of_tickets():

url = 'https://mosmetro.ru/passengers/information/special-tickets/'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')
tickets_info = soup.find_all('p')
today_date = datetime.date.isoformat(datetime.date.today()).split('-')
today_date.reverse()
day = int(today_date[0]) - 1 #не учел если дата == 1 ))))
month = int(today_date[1])
year = int(today_date[2])
last_day = calendar.monthrange(year,month)[-1]
today_date.clear()
week_list = []
for _ in range(8):
    if day == last_day:
        day = 1
        if day < 10:
            day_next = '0' + str(day)
            today_date.insert(0, day_next)
            day = int(day_next)
        if month == 12:
            month = 1
        else:
            month += 1
            if month < 10:
                month_next = '0' + str(month)
                today_date.append(month_next)
                month = int(month_next)
    else:
        if day != last_day:
            today_date.append(str(month))
        day += 1
        if day < 10:
            day_next = '0' + str(day)
            today_date.insert(0, day_next)
            day = int(day_next)
        else:
            today_date.insert(0, str(day))
    today_date.append(str(year))
    today_date.insert(1, '.')
    today_date.insert(3, '.')
    sum_date = today_date[0] + today_date[1] + today_date[2] + today_date[3] + today_date[4]
    week_list.append(sum_date)
    print(today_date, week_list)
    today_date.clear()

today_dateT = '08.11.2021' #example
for tickets_info in tickets_info:
    if today_dateT in tickets_info.text:
        print(*tickets_info, sep='')
