# 1. Написать программу, которая собирает входящие письма из своего или тестового почтового ящика,
# и сложить информацию о письмах в базу данных (от кого, дата отправки, тема письма, текст письма).


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.chrome.options import Options
from pymongo import MongoClient


client = MongoClient('localhost', 27017)
db = client['mails']
emails_col = db.emails_col

chrome_options = Options()
chrome_options.add_argument('start-maximized')

driver = webdriver.Chrome()
driver.get('https://m.mail.ru/')

assert "Mail.Ru" in driver.title

log_in = driver.find_element_by_xpath("//div[@class='social']/a").get_attribute('href')
driver.get(log_in)

elem = driver.find_element_by_xpath("//input[@type='text']")
elem.send_keys('****')

domain = driver.find_element_by_xpath("//select[@name='Domain']")
options = domain.find_elements_by_tag_name('option')
for option in options:
    if option.text == 'mail.ru':
        option.click()

elem = driver.find_element_by_xpath("//input[@type='password']")
elem.send_keys('****')

elem.send_keys(Keys.RETURN)

page = 1
letter_number = 1

while True:
    next_page = driver.find_element_by_xpath("//a[@class='pager__arrow']").get_attribute("href")
    mails = driver.find_elements_by_xpath("//a[@class='messageline__link']")
    list_of_mails = []
    for mail in mails:
        link = mail.get_attribute('href')
        list_of_mails.append(link)

    for letter in list_of_mails:
        driver.get(letter)
        time.sleep(4)
        sender = driver.find_element_by_xpath("//div[@class='readmsg__text-container__inner-line']//strong").text
        date = driver.find_element_by_xpath("//span[@class='readmsg__mail-date']").text
        theme = driver.find_element_by_xpath("//span[@class='readmsg__theme']").text
        text = driver.find_elements_by_xpath("//tbody//tr//span")
        list_of_text = []
        for t in text:
            list_of_text.append(t.text)
        full_text = " ".join(list_of_text)
        print(f'Посмотрели письмо номер {letter_number} на странице номер {page}.')
        if emails_col.count_documents({'link': letter}) == 0:
            emails_col.insert_one({
                'link': letter,
                'sender': sender,
                'date': date,
                'theme': theme,
                'full_text': full_text
            })
            print(f'..и добавили его в базу.')
        letter_number += 1
    if next_page is None:
        break
    else:
        driver.get(next_page)
        letter_number = 1
        page += 1




