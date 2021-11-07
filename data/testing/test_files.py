import requests
from bs4 import BeautifulSoup
import pandas as pd

bank_id = 1771062 #ID банка на сайте banki.ru
page=1
max_page=10

url = 'https://www.banki.ru/services/questions-answers/?id=%d&p=%d' % (bank_id, page)
r = requests.get(url)
with open('test.html', 'w') as output_file:
  output_file.write(r.text)