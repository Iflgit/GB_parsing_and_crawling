import matplotlib.pyplot as plt
import csv
from datetime import datetime


types = set()
dates = set()
regions = set()
data = list()

with open('opendata.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        _name = row['name']
        types.add(_name)

        _date = datetime.strptime(row['date'], '%Y-%m-%d')
        dates.add(_date)

        _region = row['region']
        regions.add(_region)

        data.append([
            _name, 
            _region, 
            _date, 
            int(row['value'])])

report = input(f'\nEnter report type {types}: ')
if not report:
    report = 'Средняя зарплата'

date_start = input(f'\nStart date (from {min(dates).date()} to {max(dates).date()}): ')
if not date_start:
    date_start = min(dates)
else:
    try:
        date_start = datetime.strptime(date_start, '%Y-%m-%d')
    except:
        print(f'wrong date, using {min(dates)}')
        date_start = min(dates)

date_finish = input(f'\nEnd date (from {min(dates).date()} to {max(dates).date()}): ')
if not date_finish:
    date_finish = max(dates)
else:
    try:
        date_finish = datetime.strptime(date_finish, '%Y-%m-%d')
    except:
        print(f'wrong date, using {max(dates)}')
        date_finish = max(dates)

region = input(f'\nInput region from {regions}: ')
if not region:
    region = 'Россия'

money = []
date = []

for row in data:
    if row[0] == report and row[1] == region and date_start <= row[2] <= date_finish:
        date.append(row[2])
        money.append(row[3])

if date and money:
    plt.plot(date, money)
    plt.show()
else:
    print(f'No data found')
