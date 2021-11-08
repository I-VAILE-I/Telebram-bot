import requests
from bs4 import BeautifulSoup

url = 'https://mosmetro.ru/passengers/information/special-tickets/'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')
tickets_info = soup.find_all('p')
today_date = '08.11.2021' #example

for tickets_info in tickets_info:
    if today_date in tickets_info.text:
        print(*tickets_info, sep='')
