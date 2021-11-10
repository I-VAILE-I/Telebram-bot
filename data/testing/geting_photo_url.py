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
kolvo = 1 * 2 # 1 text about ticket = 2 tickets photo
for i in range(kolvo):
    otriv = 0
    rashodnik = str(photo_url[i]) + '"'
    #print(b)
    rashodnik.split('"')
    for j in range(len(rashodnik)):
        #print(b[j])
        if rashodnik[j] == '"' and otriv != 1:
            znach = True
            otriv += 1
            inde_X = j + 1
            while znach == True:
                img_url.append(rashodnik[inde_X])
                inde_X += 1
                if rashodnik[inde_X] == '"':
                    znach = False
            #print(*img_url, sep='')
            photo_url_ = 'https://mosmetro.ru' + ''.join(img_url)
            photo.append(photo_url_)
            img_url.clear()
print(photo)