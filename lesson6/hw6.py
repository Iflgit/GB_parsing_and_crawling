'''
1) Написать программу, которая собирает входящие письма из своего или 
тестового почтового ящика и сложить данные о письмах в базу данных 
(от кого, дата отправки, тема письма, текст письма)

2) Написать программу, которая собирает «Хиты продаж» с сайтов техники 
mvideo, onlinetrade и складывает данные в БД. Магазины можно выбрать свои. 
Главный критерий выбора: динамически загружаемые товары'''

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By 


chrome = webdriver.Chrome()
chrome.get('https://mail.ru')
assert 'Mail.ru' in chrome.title
chrome.implicitly_wait(3000)
save_checkbox = WebDriverWait(chrome, 10).until(EC.presence_of_element_located((By.ID, "mailbox:saveauth")) )


# driver.wait.until(lambda driver: driver.find_element_by_id('mailbox:saveauth'))
# save_checkbox = chrome.find_element_by_id("mailbox:saveauth")
assert save_checkbox.get_attribute('type') == 'checkbox'

if save_checkbox.is_selected():
    save_checkbox.click()

WebDriverWait(chrome, 10).until(EC.presence_of_element_located((By.ID, "mailbox:login"))).send_keys('geektest10')
pass_field = WebDriverWait(chrome, 10).until(EC.presence_of_element_located((By.ID, "mailbox:password")))
pass_field.send_keys('Sample10' + Keys.RETURN)

data = WebDriverWait(chrome, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "b-datalists")))
data_list = data.find_elements_by_class_name('b-datalist__item__body')
print(len(data_list))
for mail in data_list:
    if 'рассылки' in mail.find_element_by_tag_name('a').get_attribute('text').lower():
        continue
    mail_href = mail.find_element_by_tag_name('a').get_attribute('href')
    chrome.get(mail_href)
    # mail_title = mail.find_element_by_tag_name('a').get_attribute('title')

# WebDriverWait(chrome, 10).until(EC.presence_of_element_located((By.TAG_NAME, "input"))).click()\