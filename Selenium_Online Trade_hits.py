# Написать программу, которая собирает «Хиты продаж» с сайтов техники М.видео, ОНЛАЙН ТРЕЙД и складывает данные в БД.
# Магазины можно выбрать свои. Главный критерий выбора: динамически загружаемые товары.

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from pymongo import MongoClient



client = MongoClient('localhost', 27017)
db = client['goods']
goods_col = db.goods_col

chrome_options = Options()
chrome_options.add_argument('start-maximized')

driver = webdriver.Chrome()
main_link = 'https://www.onlinetrade.ru/'
driver.get(main_link)

time.sleep(5)

assert "ОНЛАЙН ТРЕЙД" in driver.title

block_hits = driver.find_element_by_id("tabs_hits")

items = block_hits.find_elements_by_xpath(".//div[@class='indexGoods__item']")

good_added = 0

for item in items:
    link = item.find_element_by_xpath(".//div[@class='indexGoods__item__descriptionCover']/a").get_attribute('href')
    name = item.find_element_by_xpath(".//div[@class='indexGoods__item__descriptionCover']/a").text
    if name == '':
        next_button = block_hits.find_element_by_xpath("../..//span[@class='swiper-button-next ic__hasSet ic__hasSet__arrowNextBlue']")
        next_button.click()
        time.sleep(5)
    name = item.find_element_by_xpath(".//div[@class='indexGoods__item__descriptionCover']/a").text
    if name != '':
        name = item.find_element_by_xpath(".//div[@class='indexGoods__item__descriptionCover']/a").text
        price = item.find_element_by_xpath(".//div[@class='indexGoods__item__price']/span").text
        price_split = price.split()
        price_split.pop()
        price_pure = float(''.join(price_split))
        if goods_col.count_documents({'link': link}) == 0:
            goods_col.insert_one({
                'productName': name,
                'productPriceLocal': price_pure,
                'link': link,
                'source': main_link
            })
            good_added += 1

print(f'Добавлено значений в базу: {good_added}')


