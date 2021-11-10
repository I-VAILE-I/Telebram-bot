import requests
from bs4 import BeautifulSoup

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



img_url = []
photo = []
znach = False
otriv = 0
kolvo = 1 * 2 # 1 text about ticket = 2 tickets photo
# for i in range(kolvo):
#     otriv = 0
#     rashodnik = str(photo_url[i]) + '"'
#     rashodnik.split('"')
#     for j in range(len(rashodnik)):
#         if rashodnik[j] == '"' and otriv != 1:
#             znach = True
#             otriv += 1
#             inde_X = j + 1
#             while znach == True:
#                 img_url.append(rashodnik[inde_X])
#                 inde_X += 1
#                 if rashodnik[inde_X] == '"':
#                     znach = False
#             photo_url_ = 'https://mosmetro.ru' + ''.join(img_url)
#             photo.append(photo_url_)
#             img_url.clear()

# print(photo[0], photo[1])
tickets_photos(photo_url, otriv, kolvo, znach, photo, img_url)