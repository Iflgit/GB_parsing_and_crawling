'''
1) Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB 
и реализовать функцию, записывающую собранные объявления с avito.ru в 
созданную БД (xpath/BS для парсинга на выбор)
2) Написать функцию, которая производит поиск и выводит на экран объявления 
с ценой меньше введенной суммы
*Написать функцию, которая будет добавлять в вашу базу данных 
только новые объявления
'''

import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from pymongo.errors import BulkWriteError, ServerSelectionTimeoutError


def request_to_site():
    try:
        request = requests.get('https://www.avito.ru/rossiya/hobbi_i_otdyh')
        return request.text
    except requests.exceptions.ConnectionError:
        print('Please check your internet connection!')
        exit(1)

def get_adverts():
    result = []
    html_doc = request_to_site()
    soup = BeautifulSoup(html_doc, 'html.parser')
    adverts = soup.find_all('div', {'class': 'item_table-header'})
    for advert in adverts:
        advert_caption = advert.find('a')
        advert_title = advert_caption.text
        advert_href = f"https://www.avito.ru{advert_caption['href']}"

        advert_price = advert.find('span', {'itemprop':'price'})['content']

        result.append({
            'title': advert_title,
            'price': int(advert_price),
            'href': advert_href
        })

    return result

def save_to_mongo_db():
    client = MongoClient('mongodb://127.0.0.1:27017')
    db = client['avito_adverts']
    adverts_db = db.avito_adverts
    try:
        adverts_db.create_index("href", unique = True)
    except ServerSelectionTimeoutError:
        print(f'Erorr. Check your mongodb server')
        exit(1)

    # uncomment this line for only new results
    # adverts_db.drop()

    try:
        adverts_db.insert_many(get_adverts(), ordered=False)
    except BulkWriteError:
        print('duplicates droped')


def get_cheaper(price):
    client = MongoClient('mongodb://127.0.0.1:27017')
    db = client['avito_adverts']
    adverts_db = db.avito_adverts
    price_query = {"price": {"$lt": price}}

    chipiests = adverts_db.find(price_query)
    return chipiests

save_to_mongo_db()

highest_price = int(input('Enter highest price: '))

try:
    for chip in get_cheaper(highest_price):
        if chip['price'] > 0:
            print(chip['title'], chip['price'], chip['href'], sep='***')
except ServerSelectionTimeoutError:
    print('Error. Check your mongodb server')




