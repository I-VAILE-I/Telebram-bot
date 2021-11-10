import requests
from bs4 import BeautifulSoup

url = 'https://mosmetro.ru/passengers/information/special-tickets/'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')
photo_url = soup.find_all(width="333")
print(photo_url)
img_url = []
photo = []
znach = False
otriv = 0
for i in range(2):
    b = str(photo_url[i]) + '"'
    #print(b)
    b.split('"')
    for j in range(len(b)):
        #print(b[j])
        if b[j] == '"' and otriv != 1:
            znach = True
            otriv += 1
            inde_X = j + 1
            while znach == True:
                img_url.append(b[inde_X])
                inde_X += 1
                if b[inde_X] == '"':
                    znach = False
            #print(*img_url, sep='')
            photo_url_ = 'https://mosmetro.ru' + ''.join(img_url)
            photo.append(photo_url_)
            img_url.clear()
