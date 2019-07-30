'''Урок 4. Парсинг HTML (Xpath/BeautifulSoup)
1) С помощью BeautifulSoup спарсить новости с https://news.yandex.ru по своему региону.
*Заголовок
*Краткое описание
*Ссылка на новость
2) * Разбить новости по категориям
* Расположить в хронологическом порядке
'''
import requests
from bs4 import BeautifulSoup

USER_AGENT = 'User-Agent: Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'

def request_to_site():

    headers = {'accept': '*/*','user-agent': USER_AGENT}

    params = {}

    try:
        response = requests.get('https://news.yandex.by/Moscow/index.html', headers=headers, params=params)
        return response.text
    except requests.exceptions.ConnectionError:
        print('Please check your internet connection!')
        exit(1)


def get_site_name(url):
    from urllib.parse import urlparse
    parsed_uri = urlparse(url)
    return f'{parsed_uri.scheme}://{parsed_uri.netloc}'


def parse_news():
    html_doc = request_to_site()
    soup = BeautifulSoup(html_doc, 'html.parser')
    news = soup.findAll('div', {'class': 'story'})
    for index, story in enumerate(news):
        _story_time = story.find('div', {'class': 'story__date'}).string.split()[-1]
        _story_div = story.find('div', {'class': 'story__text'})
        if not _story_div:
            _story_text =''
        else:
            _story_text = _story_div.text
        _hrefs = story.findAll('a')
        _story_topic = _hrefs[1].text
        _story_rubric = _hrefs[0].text
        _story_rubric_href = _hrefs[0]['href']
        _story_href = _hrefs[1]['href']
        print(index, _story_time, _story_rubric, _story_topic, sep='-'*5)
        print(_story_text, f'{get_site_name(_story_rubric_href)}{_story_href}')
        print('-'*40)


parse_news()
