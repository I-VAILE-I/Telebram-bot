import requests
from bs4 import BeautifulSoup
import datetime
import calendar

def availability_of_tickets(tickets_info, loop_list, day, month, year, last_day, week_list):
    for _ in range(8):  # week dates loop
        if day == last_day:
            day = 1
            day_next = '0' + str(day)
            loop_list.insert(0, day_next)
            day = int(day_next)
            if month == 12:
                month = 1
                month_next = '0' + str(month)
                loop_list.insert(1, month_next)
                month = int(month_next)
                year += 1
                loop_list.append(str(year))
            else:
                month += 1
                if month < 10:
                    month_next = '0' + str(month)
                    loop_list.insert(1, month_next)
                    month = int(month_next)
        else:
            if day != last_day:
                if month < 10:
                    month_next = '0' + str(month)
                    loop_list.append(month_next)
                    month = int(month_next)
                else:
                    loop_list.append(str(month))
            day += 1
            if day < 10:
                day_next = '0' + str(day)
                loop_list.insert(0, day_next)
                day = int(day_next)
            else:
                loop_list.insert(0, str(day))
        loop_list.append(str(year))
        loop_list.insert(1, '.')
        loop_list.insert(3, '.')
        sum_date = ''.join(loop_list)
        week_list.append(sum_date)
        loop_list.clear()
    for tickets_info in tickets_info:
        for i in range(len(week_list)):
            search_date = week_list[i]
            if search_date in tickets_info.text:
                name_ticket = ''.join(tickets_info)
                return name_ticket


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

print(only_tickets)

loop_list = []

day = 11 -1
month = 11
year = 2020
#
# #day = int(today_date[0]) -1
# #month = int(today_date[1])
# #year = int(today_date[2])

last_day = calendar.monthrange(year,month)[-1]
week_list = []

for _ in range(8): #week dates loop
    if day == last_day:
        day = 1
        day_next = '0' + str(day)
        loop_list.insert(0, day_next)
        day = int(day_next)
        if month == 12:
            month = 1
            month_next = '0' + str(month)
            loop_list.insert(1, month_next)
            month = int(month_next)
            year += 1
            loop_list.append(str(year))
        else:
            month += 1
            if month < 10:
                month_next = '0' + str(month)
                loop_list.insert(1, month_next)
                month = int(month_next)
    else:
        if day != last_day:
            if month < 10:
                month_next = '0' + str(month)
                loop_list.append(month_next)
                month = int(month_next)
            else:
                loop_list.append(str(month))
        day += 1
        if day < 10:
            day_next = '0' + str(day)
            loop_list.insert(0, day_next)
            day = int(day_next)
        else:
            loop_list.insert(0, str(day))
    loop_list.append(str(year))
    loop_list.insert(1, '.')
    loop_list.insert(3, '.')
    sum_date = ''.join(loop_list)
    week_list.append(sum_date)
    loop_list.clear()

#print(today_date, week_list)


for tickets_info in tickets_info:
    for i in range(len(week_list)):
        search_date = week_list[i]
        if search_date in tickets_info.text:
            print(*tickets_info, sep='')

# availability_of_tickets(tickets_info, loop_list, day, month, year, last_day, week_list)
