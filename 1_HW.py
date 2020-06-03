# 1. Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев для конкретного пользователя,
# сохранить JSON-вывод в файле *.json.

import requests
import json
from pprint import pprint

my_page = 'natalyaburmistrova91'
service = f'https://api.github.com/users/{my_page}/repos'
req = requests.get(service)
data = req.json()
list_of_repos = []
for i in data:
    list_of_repos.append(i['full_name'])
pprint(list_of_repos)

with open("data_file.json", "w", encoding="utf-8") as file1:
    json.dump(data, file1)

# 2. Изучить список открытых API. Найти среди них любое, требующее авторизацию (любого типа).
# Выполнить запросы к нему, пройдя авторизацию. Ответ сервера записать в файл.

api_key='18008e360b28d0a2361e28b041da7f08'
country = 'Spain'

params = {
    'method': 'geo.gettopartists',
    'country': country,
    'api_key': api_key,
    'format':'json'
          }
link = 'http://ws.audioscrobbler.com/2.0/'
response = requests.get(link, params=params)
music_data = response.json()
country_server = music_data['topartists']['@attr']['country']
artists_data = music_data['topartists']['artist']
top_artists = []
for i in artists_data:
    top_artists.append(i['name'])
print(f'В стране {country_server} топовыми артистами являются:')
for i in range(len(top_artists)):
    print(f'{i + 1}. {top_artists[i]}')

with open("data_music.json", "w", encoding="utf-8") as file2:
    json.dump(music_data, file2)