# 1)Написать приложение, которое собирает основные новости с сайтов news.mail.ru, lenta.ru, yandex.news
# Для парсинга использовать xpath. Структура данных должна содержать:
# название источника,
# наименование новости,
# ссылку на новость,
# дата публикации
#
# 2)Сложить все новости в БД


import requests
from pymongo import MongoClient
from pprint import pprint
from lxml import html


def main_mail_news_collector():
    client = MongoClient('localhost', 27017)
    db = client['news']
    news_col = db.news_col
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
        'Accept': '*/*'}
    main_link = 'https://news.mail.ru'
    response = requests.get(main_link, headers=header)
    dom = html.fromstring(response.text)
    news = dom.xpath("//a[@class='newsitem__title link-holder']/@href")
    news_added = 0
    for link_end in news:
        response_item = requests.get(f'{main_link}{link_end}', headers=header)
        dom_item = html.fromstring(response_item.text)
        source = dom_item.xpath("//a[@class='link color_gray breadcrumbs__link']/@href")
        name_item = dom_item.xpath("//h1[@class='hdr__inner']/text()")
        datetime = dom_item.xpath("//span[@class='note__text breadcrumbs__text js-ago']/@datetime")

        if news_col.count_documents({'link': f'{main_link}{link_end}'}) == 0:
            news_col.insert_one({
                "name_news": name_item,
                "link": f'{main_link}{link_end}',
                "datetime": datetime,
                "source": source
            })
            news_added += 1
    pprint(f'Добавлено позиций из {main_link}: {news_added}')


def main_lenta_news_collector():
    client = MongoClient('localhost', 27017)
    db = client['news']
    news_col = db.news_col

    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
        'Accept': '*/*'}
    main_link = 'https://lenta.ru'
    response = requests.get(main_link, headers=header)
    dom = html.fromstring(response.text)
    link = dom.xpath("//section[@class='row b-top7-for-main js-top-seven']//div[@class='item']//a/@href")
    news_added = 0

    for link_end in link:
        datetime = dom.xpath(f"//section[@class='row b-top7-for-main js-top-seven']//div[@class='item']//a[@href='{link_end}']//time[@class='g-time']/@datetime")
        name_item_durty = dom.xpath(f"//section[@class='row b-top7-for-main js-top-seven']//div[@class='item']//a[@href='{link_end}']/text()")
        name_item_pure = name_item_durty[0].replace("\xa0", " ")

        if news_col.count_documents({'link': f'{main_link}{link_end}'}) == 0:
            news_col.insert_one({
                "name_news": name_item_pure,
                "link": f'{main_link}{link_end}',
                "datetime": datetime[0],
                "source": main_link
            })

            news_added += 1
    pprint(f'Добавлено позиций из {main_link}: {news_added}')


def yandex_news_collector():
    client = MongoClient('localhost', 27017)
    db = client['news']
    news_col = db.news_col

    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'}
    main_link = 'https://yandex.ru/news'
    response = requests.get(main_link, headers=header)
    dom = html.fromstring(response.text)
    blocks = dom.xpath("//div[@class='story__topic']")

    news_added = 0

    for block in blocks:
        link_end = block.xpath(".//h2[@class='story__title']/a/@href")[0]
        link = f'{main_link}{link_end}'
        name = block.xpath(".//h2[@class='story__title']/a/text()")[0]
        source_time = block.xpath("../div[@class='story__info']/div[@class='story__date']/text()")[0]
        source_time_split = source_time.split()
        time = source_time_split.pop()
        source = ' '.join(source_time_split)

        if news_col.count_documents({'link': f'{link}'}) == 0:
            news_col.insert_one({
                "name_news": name,
                "link": link,
                "datetime": time,
                "source": source
            })
            news_added += 1

    pprint(f'Добавлено позиций из {main_link}: {news_added}')


client = MongoClient('localhost', 27017)
db = client['news']
news_col = db.news_col

# практиковалась, поэтому обнуляла
# news_col.delete_many({})


# main_mail_news_collector()
# Вывод: 'Добавлено позиций из https://news.mail.ru: 6'
# Пример:
# {'_id': ObjectId('5ee74e068c985d89643ba3f5'),
#  'datetime': ['2020-06-15T09:22:46+03:00'],
#  'link': 'https://news.mail.ru/society/42186138/',
#  'name_news': ['Июльская жара ожидается на текущей неделе в Московском '
#                'регионе'],
#  'source': ['https://riamo.ru/']}

# main_lenta_news_collector()
# Вывод: 'Добавлено позиций из https://lenta.ru: 9'
# Пример:
# {'_id': ObjectId('5ee74e078c985d89643ba3fd'),
#  'datetime': ' 13:26, 15 июня 2020',
#  'link': 'https://lenta.ru/news/2020/06/15/moroz/',
#  'name_news': 'Единственная украинка в UFC рассказала о работе дояркой и '
#               'грузчицей',
#  'source': 'https://lenta.ru'}

# yandex_news_collector()
# Вывод: 'Добавлено позиций из https://yandex.ru/news: 65'
# Пример:
# {'_id': ObjectId('5ee74e088c985d89643ba408'),
#  'datetime': '13:16',
#  'link': 'https://yandex.ru/news/news/story/Sobyanin_soobshhil_o_novom_ehtape_snyatiya_ogranichenij--601a09356fa32857c2886784a408fbe6?lr=213&lang=ru&stid=gF0UMVgu4QgB_aaD1Iq3&persistent_id=102609603&rubric=index&from=index',
#  'name_news': 'Собянин сообщил о новом этапе снятия ограничений',
#  'source': 'Вести.Ru'}

#проверка

print(f'Всего документов в базе: {news_col.count_documents({})}')
# Вывод: 'Всего документов в базе: 80'

# for news in news_col.find({}):
#     pprint(news)
# Вывод в примерах в функции
