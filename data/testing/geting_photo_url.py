import requests
from bs4 import BeautifulSoup

url = 'https://mosmetro.ru/passengers/information/special-tickets/'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')
photo_url = soup.find_all(width="333")
print(photo_url)
img_url = []
znach = False

for i in range(2):
    b = str(photo_url[i]) + '"'
    #print(b)
    b.split('"')
    for j in range(len(b)):
        #print(b[j])
        if b[j] == '"':
            znach = True
            inde_X = j
            while znach == True:
                inde_X += 1
                if b[inde_X] == '"':
                    znach = False
                img_url.append(b[inde_X])
            print(*img_url)