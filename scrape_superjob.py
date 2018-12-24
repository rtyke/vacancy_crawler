import json
from typing import Dict, List
import os

import requests

from utils import get_unixtime_month_back, get_unixtime_halfhour_back
from data_handling_json import grab_newest_file_content, save_to_json


SECRET_KEY = os.environ['KEY']

HEADERS = {'X-Api-App-Id': SECRET_KEY}


def request_page_with_vacancies(from_date, until_date: int):
    vacancies_url = 'https://api.superjob.ru/2.0/vacancies/'
    params = {
        'count': 100,
        'page': 0,
        'date_published_from': from_date,
        'date_published_to': until_date,
    }
    try:
        response = requests.get(vacancies_url, headers=HEADERS, params=params)
        response.raise_for_status()
        return response
    except requests.RequestException:
        print('Connection error')
        return False


def scrape_vacancies(from_date: int, until_date: int):
    page_with_vacancies = request_page_with_vacancies(from_date, until_date)
    if page_with_vacancies:
        vacancies_on_page = page_with_vacancies.json().get('objects')
        print('total: ', page_with_vacancies.json()['total'])
        print('more: ', page_with_vacancies.json()['more'])
        if not vacancies_on_page:
            return False
        return vacancies_on_page
    print('Connections issues')
    return False  # return False in case of bad internet connection


def define_oldest_vacancy_timestamp(vacancies_all: List[Dict]) -> int:
    return min([vacancy['date_published'] for vacancy in vacancies_all])


def get_last_month_vacancies():
    month_back = get_unixtime_month_back()
    halfhour_back = get_unixtime_halfhour_back()
    from_date, until_date = month_back, halfhour_back
    while True:
        vacancies_chunk = scrape_vacancies(
            from_date=from_date,
            until_date=until_date)
        if vacancies_chunk:
            until_date = define_oldest_vacancy_timestamp(vacancies_chunk)
            yield vacancies_chunk
        else:
            break


def scrape_new_vacancies(from_date):
    halfhour_back = get_unixtime_halfhour_back()
    vacancies_new = scrape_vacancies(
        from_date=from_date,
        until_date=halfhour_back)
    return vacancies_new


def get_vacancy_by_id(id):
    """
    Doesn't work properly because of vague SuperJob API
    """
    url = 'https://api.superjob.ru/2.0/vacancies/'
    params = {'id_vacancy': id}
    response = requests.get(url, headers=HEADERS, params=params)
    print(json.dumps(response.json(), indent=4, ensure_ascii=False))


def launch_first_time():
    # TODO move to main.py
    """
    Use this function for the first launch of the script.
    """
    vacancies_last_month = get_last_month_vacancies()
    for vacancies_chunk in vacancies_last_month:
        save_to_json(vacancies_chunk)


def update_data():
    # TODO move to main.py
    """
    Use this function only if you've doanloaded vacany data already and you
    need update.
    """
    from_date = define_oldest_vacancy_timestamp(grab_newest_file_content())
    vacancies_all = scrape_new_vacancies(from_date=from_date)
    if not vacancies_all:
        return f'No vacancies for date {from_date}'
    else:
        return vacancies_all


if __name__ == '__main__':
    launch_first_time()

