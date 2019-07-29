import requests
from lxml import html


def request_to_site():
    """Function do search to yandex.ru by user's request"""

    my_str = input('Please, enter your request here: ')
    try:
        request = requests.get('https://www.yandex.ru/search',
                               params={'text': my_str})
        root = html.fromstring(request.text)

        results_list = root.xpath(
            ".//a[contains(@class, 'link_cropped_no')]/@href")
        if results_list:
            for i in results_list:
                print(i)
        else:
            print("At your request no results were found. Please, check your request.")
            request_to_site()
    except requests.exceptions.ConnectionError:
        print("No connection to site")
        exit(1)


if __name__ == '__main__':
    request_to_site()
