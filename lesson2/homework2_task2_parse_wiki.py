import collections
import requests
import re


def return_wiki_html(topic):
    wiki_request = requests.get(f'https://ru.wikipedia.org/wiki/{topic.capitalize()}')
    return wiki_request.text

# def return_words(topic):
#     wiki_html = return_wiki_html(topic)
#     words = re.findall('[а-яА-Я]{3,}', wiki_html)
#     words_counter = collections.Counter()
#     for word in words:
#         words_counter[word] += 1
#     for word in words_counter.most_common(10):
#         print(f'Слово {word[0]} встречается {word[1]} раз')
#     return words_counter.most_common(10)


def return_words_any(link):
    # wiki_html = return_wiki_html(topic)
    try:
        req = requests.get(link)
    except:
        return []
    words = re.findall('[а-яА-Я]{3,}', req.text)
    words_counter = collections.Counter()

    for word in words:
        words_counter[word] += 1

    # for word in words_counter.most_common(10):
    #     print(f'Слово {word[0]} встречается {word[1]} раз')
    return words_counter.most_common(10)

# print(return_words('Трям!_Здравствуйте!'))
# print(return_wiki_html('Беларусь'))
links = re.findall(r'href="(http\S*)"', return_wiki_html('Белоруссия'))
links_count = len(links)
for indx, link in enumerate(links):
    # print(link)
    if 'wiki' not in link:
        print(f'{indx}/{links_count}', link, return_words_any(link))

