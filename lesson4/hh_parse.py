import requests
from lxml import html

USER_AGENT = 'User-Agent: Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'

def request_to_site():
    headers = {
        'accept': '*/*',
        'user-agent': USER_AGENT
    }
    params = {
        'text': 'программист'
    }
    try:
        request = requests.get(
            'https://hh.ru/search/vacancy',
            headers=headers,
            params=params)
        return request.text
    except requests.exceptions.ConnectionError:
        print('Please check your internet connection!')
        exit(1)


def parse_vacancies():
    #get lxml.html object
    html_page = html.fromstring(request_to_site())
    #get div's with data
    vacancies = html_page.xpath("//div[contains(@class, 'item__row_header')]")
    print(f'{len(vacancies)} vacantcies found')
    for vacancy in vacancies:
        #get text in <a href>
        print(vacancy.xpath('.//a/text()')[0])
        #get value of href attribute
        print(vacancy.xpath('.//a/@href')[0])
        try:
            print(vacancy.xpath('.//div[contains(@class, "item__compensation")]/text()')[0])
        except IndexError:
            print('Зарплата не указана')
        print('~' * 25)


parse_vacancies()
