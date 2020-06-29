from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


chrome_options = Options()
chrome_options.add_argument('start-maximized')

driver = webdriver.Chrome(options = chrome_options)

driver.get('https://lenta.com/catalog/frukty-i-ovoshchi/')

button = driver.find_element_by_class_name('store-notification__button--submit')
button.click()

button = WebDriverWait(driver,5).until(
    EC.element_to_be_clickable((By.CLASS_NAME, 'store-notification__button--submit'))
)

button.click()

driver.execute_script('window.scrollTo(0, 2000)')

button = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.CLASS_NAME, 'cookie-usage-notice__button'))
    )
button.click()

while True:
    try:
        button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'catalog-grid-container__pagination-button'))
        )
        # driver.execute_script('window.scrollHeight')
        button.click()
    except:
        break


