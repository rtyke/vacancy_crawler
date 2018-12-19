import datetime
import json
import time
from typing import Dict, List
import os

import requests


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


def unixtime_from_datetime(date_to_convert):
    # TODO move to another module
    return int(time.mktime(date_to_convert.timetuple()))


def get_unixtime_halfhour_back():
    # TODO move to another module
    halfhour_back = datetime.datetime.today() - datetime.timedelta(minutes=30)
    return unixtime_from_datetime(halfhour_back)


def get_unixtime_month_back():
    # TODO move to another module
    month_back = datetime.datetime.today() - datetime.timedelta(days=30)
    return unixtime_from_datetime(month_back)


def save_to_json(data_to_save):
    json_name = f'{int(time.time())}.json'
    json_folder = os.path.join(os.getcwd(), 'jsons')
    if not os.path.exists(json_folder):
        os.mkdir(json_folder)
    with open(os.path.join(json_folder, json_name), 'w') as fo:
        json.dump(data_to_save, fo, ensure_ascii=False)


def get_oldest_date():
    json_folder = os.path.join(os.getcwd(), 'jsons')
    newest_file = max(os.listdir(json_folder))
    with open(os.path.join(json_folder, newest_file)) as fo:
        vacancies = json.load(fo)
    return define_oldest_vacancy_timestamp(vacancies)


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


def main():
    # for the first launch:
    # vacancies_last_month = get_last_month_vacancies()
    # for vacancies_chunk in vacancies_last_month:
    #     save_to_json(vacancies_chunk)
    # for the next launches:
    from_date = get_oldest_date()
    vacancies_all = scrape_new_vacancies(from_date=from_date)
    if not vacancies_all:
        print(f'No vacancies for date {from_date}')
    else:
        save_to_json(vacancies_all)


if __name__ == '__main__':
    main()

