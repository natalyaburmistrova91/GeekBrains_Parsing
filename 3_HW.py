from bs4 import BeautifulSoup as bs
import requests
from pymongo import MongoClient
from pprint import pprint

# функция для обработки заработной платы
def string_salary(text):
    salary_min = None
    salary_max = None
    currency = None
    str_min = []
    str_max = []
    str_currency = []
    string_list = text.split()
    string = ''.join(string_list)
    if string[0] == 'о':
        for i in range(2, len(string)):
            if string[i].isdigit():
                str_min.append(string[i])
            else:
                str_currency.append(string[i])
        salary_min = float(''.join(str_min))
        currency = ''.join(str_currency)
    elif string[0] == 'д':
        for i in range(2, len(string)):
            if string[i].isdigit():
                str_max.append(string[i])
            else:
                str_currency.append(string[i])
        salary_max = float(''.join(str_max))
        currency = ''.join(str_currency)
    else:
        i = 0
        flag = 0
        while i < (len(string)):
            if flag == 0:
                if string[i].isdigit():
                    str_min.append(string[i])
                else:
                    flag = 1
            else:
                if string[i].isdigit():
                    str_max.append(string[i])
                else:
                    str_currency.append(string[i])
            i += 1
        salary_max = float(''.join(str_max))
        salary_min = float(''.join(str_min))
        currency = ''.join(str_currency)
    return salary_min, salary_max, currency


# функция(генератор) для возврата результата позиции
def info_vacancy(vacancies_list):
    for i in vacancies_list:
        name_link_block = i.find('a',{'class':'bloko-link HH-LinkModifier'})
        link = name_link_block['href']
        name = name_link_block.text
        salary_block = i.find('div',{'class':'vacancy-serp-item__sidebar'})
        salary_min = None
        salary_max = None
        currency = None
        if salary_block.text != '':
            salary_min, salary_max, currency = string_salary(salary_block.text)
        yield name, link, salary_min, salary_max, currency, 'hh.ru'


# функция для заполнения базы вакансиями
def collector_of_vacancies(vacancy):
    client = MongoClient('localhost', 27017)
    db = client['vacancies']
    vacancies_col = db.vacancies_col
    headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
    'Accept': '*/*'}
    main_link = 'https://www.hh.ru'
    k = 0
    while True:
        params = {
            'clusters': 'true',
            'enable_snippets': 'true',
            'st': 'searchVacancy',
            'text': vacancy,
            'fromSearch': 'true',
            'page': k
        }
        response = requests.get(f'{main_link}/search/vacancy', headers=headers, params=params)
        soup = bs(response.text, 'html.parser')
        vacancy_block = soup.find('div', {'class': 'vacancy-serp'})
        if vacancy_block is None:  # на всякий случай сделала 2 проверки
            break
        vacancies_list = vacancy_block.findAll('div', {'class': 'vacancy-serp-item'})
        vacancies = info_vacancy(vacancies_list)
        for i in vacancies:
            name, link, salary_min, salary_max, currency, source = i
            vacancies_col.insert_one({
                "name": name,
                "link": link,
                "salary_min": salary_min,
                "salary_max": salary_max,
                "currency": currency,
                "source": source
            })
        check_page = soup.find('a', {'class': 'bloko-button HH-Pager-Controls-Next HH-Pager-Control'})
        if check_page is not None:  # вот вторая проверка
            k += 1
        else:
            break


# Фукнция для поиска подходящей по зп вакансии
def luxary_salary_founder(dream):
    for vac in vacancies_col.find({'$or': [{'$and': [{'salary_min': {'$lte': dream}}, {'salary_max': {'$eq': None}}]},
                                           {'salary_max': {'$gte': dream}}]}):
        pprint(vac)


vacancy = 'юрист'
client = MongoClient('localhost', 27017)
db = client['vacancies']
vacancies_col = db.vacancies_col

# практиковалась, поэтому обнуляла
# vacancies_col.delete_many({})
# функция, которая заносит информацию в БД
# collector_of_vacancies(vacancy)
# проверка
# print(vacancies_col.count_documents({}))
# вывод 2000


request = 100000
luxary_salary_founder(request)

# пример части вывода:

# {'_id': ObjectId('5ee17727cbeea237f39b1447'),
#  'currency': 'руб.',
#  'link': 'https://hh.ru/vacancy/37444749?query=%D1%8E%D1%80%D0%B8%D1%81%D1%82',
#  'name': 'Юрист',
#  'salary_max': None,
#  'salary_min': 45000.0,
#  'source': 'hh.ru'}
# {'_id': ObjectId('5ee17727cbeea237f39b1448'),
#  'currency': 'руб.',
#  'link': 'https://hh.ru/vacancy/37072140?query=%D1%8E%D1%80%D0%B8%D1%81%D1%82',
#  'name': 'Юрист первичного приёма/Менеджер по продажам юридических услуг',
#  'salary_max': 400000.0,
#  'salary_min': 100000.0,
#  'source': 'hh.ru'}