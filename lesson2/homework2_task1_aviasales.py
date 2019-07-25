"""
Задание 1. Доработать приложение по поиску авиабилетов, чтобы оно возвращало
билеты по названию города, а не по IATA коду. Пункт отправления и пункт
назначения должны передаваться в качестве параметров. Сделать форматированный
вывод, который содержит в себе пункт отправления, пункт назначения, дату вылета,
цену билета (можно добавить еще другие параметры по желанию)
"""

import requests
from sys import argv


class IATACode:

    API_URL = 'http://api.travelpayouts.com/data/ru/cities.json'

    _cities_req: requests.sessions = None
    _IATA_codes = {}

    def __init__(self):
        try:
            self._cities_req = requests.get(self.API_URL)
        except requests.RequestException:
            print(f"can't get data from {self.API_URL}")
            exit(code=1)

        for record in self._cities_req.json():
            # print(record['name'],
            #       *record['cases'].values(),
            #       *record['name_translations'].values(),
            #       record['code'])

            _code = record['code']

            _name = record['name']
            if _name is not None:
                self._IATA_codes[_name] = _code

            for case in record['cases'].values():
                if (case is not None) and (case != ''):
                    self._IATA_codes[case] = _code

            _trans_name = record['name_translations'].values()
            self._IATA_codes[str(*_trans_name)] = _code
        # print(self._IATA_codes)

    def get_code_by_name(self, name):
        try:
            return self._IATA_codes[name]
        except KeyError:
            return ''


iata = IATACode()

assert iata.get_code_by_name('Minsk') == 'MSQ'
assert iata.get_code_by_name('Минск') == 'MSQ'
assert iata.get_code_by_name('Минску') == 'MSQ'
assert iata.get_code_by_name('Минска') == 'MSQ'
assert iata.get_code_by_name('в Минск') == 'MSQ'

assert iata.get_code_by_name('Moscow') == 'MOW'
assert iata.get_code_by_name('Москва') == 'MOW'
assert iata.get_code_by_name('Москвой') == 'MOW'
assert iata.get_code_by_name('Москве') == 'MOW'
assert iata.get_code_by_name('Москвы') == 'MOW'

assert iata.get_code_by_name('NoCity') == ''

_route = 'Хочу билет на самолёт из Москвы в Минск'
if len(argv) == 1:
    _route = 'Хочу билет на самолёт из Москвы в Минск'
else:
    _route = ' '.join(argv[1:])

print(_route)

_route_codes = ''.join(list(map(lambda s: iata.get_code_by_name(s),
                            _route.split(' '))))

assert len(_route_codes) == 6, 'at least 2 cities expected in params'
print(_route_codes)

flight_params = {
    'origin': _route_codes[:3],
    'destination': _route_codes[3:],
    'one_way': 'true'
}
req = requests.get("http://min-prices.aviasales.ru/calendar_preload",
                   params=flight_params)


data = req.json()
# print(data)
# print(data['best_prices'][0])
tickets = data['best_prices']
for ticket in tickets:
    print(f"{ticket['origin']}->{ticket['destination']}: "
          f"{ticket['found_at']}, {ticket['value']}\N{ruble sign}")
    # print(ticket)

