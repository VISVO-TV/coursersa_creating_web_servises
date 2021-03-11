"""Задание по программированию: Конвертер валют"""

import requests
from bs4 import BeautifulSoup
from decimal import *


def convert(amount, cur_from, cur_to, date):
    response = requests.get('https://www.cbr.ru/scripts/XML_daily.asp',
    params={'date_req': date.replace('.', '/')})
    soup = BeautifulSoup(response.content, 'xml')

    value1 = soup.find('CharCode', text=cur_from).find_next_sibling('Value').string
    nominal1 = soup.find('CharCode', text=cur_from).find_next_sibling('Nominal').string
    cur_result1 = Decimal(float(value1.replace(',', '.'))) / Decimal(nominal1) * Decimal(amount)

    value2 = soup.find('CharCode', text=cur_to).find_next_sibling('Value').string
    nominal2 = soup.find('CharCode', text=cur_to).find_next_sibling('Nominal').string
    cur_result2 = cur_result1 / Decimal(float(value2.replace(',', '.'))) / Decimal(nominal2)
    return round(cur_result2, 4)


def main():
    a = convert(100, 'USD', 'DKK', "12.03.2021")
    print(a)


if __name__ == '__main__':
    main()
