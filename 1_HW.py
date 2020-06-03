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

# Вывод:
# ['natalyaburmistrova91/codes_for_work',
#  'natalyaburmistrova91/GeekBrains_BigData_Python',
#  'natalyaburmistrova91/GeekBrains_DataBase',
#  'natalyaburmistrova91/GeekBrains_DataBase_CourseProject',
#  'natalyaburmistrova91/GeekBrains_Python_Algoritms',
#  'natalyaburmistrova91/linux_gb']

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

# Вывод:
# В стране Spain топовыми артистами являются:
# 1. David Bowie
# 2. Radiohead
# 3. Queen
# 4. Coldplay
# 5. The Rolling Stones
# 6. Muse
# 7. The Beatles
# 8. The Cure
# 9. Daft Punk
# 10. Arctic Monkeys
# 11. Red Hot Chili Peppers
# 12. Blur
# 13. Ed Sheeran
# 14. Nirvana
# 15. Sia
# 16. Pink Floyd
# 17. Bob Dylan
# 18. Tame Impala
# 19. The Strokes
# 20. U2
# 21. Adele
# 22. Arcade Fire
# 23. The Weeknd
# 24. Calvin Harris
# 25. R.E.M.
# 26. Michael Jackson
# 27. Depeche Mode
# 28. Led Zeppelin
# 29. Lana Del Rey
# 30. The xx
# 31. The Killers
# 32. Major Lazer
# 33. The Black Keys
# 34. Foo Fighters
# 35. Rihanna
# 36. Oasis
# 37. Imagine Dragons
# 38. The Smiths
# 39. The Clash
# 40. Gorillaz
# 41. Florence + the Machine
# 42. Franz Ferdinand
# 43. Pixies
# 44. Beck
# 45. David Guetta
# 46. The White Stripes
# 47. New Order
# 48. Vetusta Morla
# 49. Drake
# 50. Metallica


