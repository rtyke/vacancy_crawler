import datetime
import time
from typing import Dict, List
import os

import requests


SECRET_KEY = os.environ['KEY']

HEADERS = {'X-Api-App-Id': SECRET_KEY}


# def request_page_with_vacancies(since_date: int, page_number: int):
def request_page_with_vacancies(till_date: int):
    vacancies_url = 'https://api.superjob.ru/2.0/vacancies/'
    params = {
        'count': 100,
        'page': 0,
        'date_published_to': till_date,
    }
    try:
        response = requests.get(vacancies_url, headers=HEADERS, params=params)
        response.raise_for_status()
        return response
    except requests.RequestException:
        print('Connection error')
        return False


def scrape_vacancies(till_date: int):
    page_with_vacancies = request_page_with_vacancies(till_date)
    if page_with_vacancies:
        vacancies_on_page = page_with_vacancies.json().get('objects')
        if not vacancies_on_page:
            return False
        valid_vacancies = filter(
            lambda x: x['date_published'] < till_date, vacancies_on_page
        )
        return list(valid_vacancies)


def get_unixtime_halfhour_back():
    halfhour_back = datetime.datetime.today() - datetime.timedelta(minutes=30)
    return int(time.mktime(halfhour_back.timetuple()))


def main():
    halfhour_back = get_unixtime_halfhour_back()
    print(halfhour_back)
    vacancies_all = scrape_vacancies(till_date=halfhour_back)
    if not vacancies_all:
        print(f'No vacancies for date {halfhour_back}')
    else:
        print(len(vacancies_all))
        for vacancy in vacancies_all:
            print(vacancy, end='\n\n')


if __name__ == '__main__':
    main()
