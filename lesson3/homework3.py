'''Необходимо собрать информацию о вакансиях на
должность программиста или разработчика с сайта
job.ru или hh.ru. (Можно с обоих сразу) Приложение
должно анализировать несколько страниц сайта.
Получившийся список должен содержать в себе:

*Наименование вакансии,
*Предлагаемую зарплату
*Ссылку на саму вакансию'''

import requests
from lxml import html
from fake_useragent import UserAgent

print(UserAgent())

def request_to_site():
    site = r'https://hh.ru/search/vacancy'
    params = {
        'text':'',
        'area':'1',
        'salary':'',
        'currency_code':'RUR',
        'experience':'doesNotMatter',
        'order_by':'relevance',
        'search_period':'',
        'items_on_page':'20',
        'no_magic':'true'
        }
    
    try:
        request = requests.get(
            site, 
            headers={'User-Agent': UserAgent().chrome}, 
            params=params)
        root = html.fromstring(request.text)
        #//a[contains(@class,"bloko-link HH-LinkModifier")]

        result_list = root.xpath('.//a[contains(@class,"bloko-link HH-LinkModifier")]/@href')
        if result_list:
            for i in result_list:
                print(i)
        else:
            print('At your request no result found')
            print(request.text)
    except Exception as err:
        print(f'Error: {err}')

if __name__ == '__main__':
    request_to_site()

