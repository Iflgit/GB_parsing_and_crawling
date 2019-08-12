from selenium import webdriver          #Основной элемент
from selenium.webdriver.common.keys import Keys    #Клавиши клавиатуры

driver = webdriver.Chrome()

driver.get('https://geekbrains.ru/login')
assert "GeekBrains" in driver.title

#Заполняем поля для ввода
elem = driver.find_element_by_id("user_email")
elem.send_keys('example-for-geekbrains@mail.ru')
elem = driver.find_element_by_id("user_password")
elem.send_keys('password-example')
elem.send_keys(Keys.RETURN)

driver.close()
