# Написать программу, которая собирает «Хиты продаж» с сайтов техники М.видео, ОНЛАЙН ТРЕЙД и складывает данные в БД.
# Магазины можно выбрать свои. Главный критерий выбора: динамически загружаемые товары.

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import json
from pymongo import MongoClient
from pprint import pprint


client = MongoClient('localhost', 27017)
db = client['goods']
goods_col = db.goods_col

chrome_options = Options()
chrome_options.add_argument('start-maximized')

driver = webdriver.Chrome()
main_link = 'https://www.mvideo.ru/'
driver.get(main_link)

time.sleep(5)

assert "М.Видео" in driver.title

blocks = driver.find_elements_by_xpath("//div[@class='h2 u-mb-0 u-ml-xs-20 u-font-normal']")

good_added = 0

for block in blocks:
    name_block_split = block.text.split()
    name_block = ' '.join(name_block_split)
    if name_block == 'Хиты продаж':
        while True:
            try:
                next_button = block.find_element_by_xpath("../../..//a[@class='next-btn sel-hits-button-next']")
                next_button.click()
                time.sleep(5)
            except:
                break
        items = block.find_elements_by_xpath("../../../..//a[@class='sel-product-tile-title']")
        for item in items:
            data = item.get_attribute('data-product-info')
            goods_dict = json.loads(data)
            if goods_col.count_documents({'productId': goods_dict['productId']}) == 0:
                goods_col.insert_one({
                    'productId': goods_dict['productId'],
                    'productCategoryName': goods_dict['productCategoryName'],
                    'productName': goods_dict['productName'],
                    'productPriceLocal': float(goods_dict['productPriceLocal']),
                    'source': main_link
                    })
                good_added += 1

print(f'Добавлено значений в базу: {good_added}')

for good in goods_col.find({}):
    pprint(good)
