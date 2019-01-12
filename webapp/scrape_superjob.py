from typing import Dict, List

import requests

from flask import current_app
from webapp.scriber import log
from webapp.utils import strtime_from_unixtime


def request_vacancies_page(scraping_period):
    from_date, until_date = scraping_period
    log(f'Get vacancies till {strtime_from_unixtime(until_date)} since {strtime_from_unixtime(from_date)}')
    vacancies_url = 'https://api.superjob.ru/2.0/vacancies/'
    params = {
        'count': 100,
        'page': 0,
        'date_published_from': from_date,
        'date_published_to': until_date,
    }
    try:
        HEADERS = {'X-Api-App-Id': current_app.config['SJ_API_KEY']}
        response = requests.get(vacancies_url, headers=HEADERS, params=params)
        response.raise_for_status()
        return response
    except requests.RequestException:
        return False


def parse_vacancies(vacancies_raw):
    vacancies_on_page = vacancies_raw.json().get('objects', None)
    log(f'total: {vacancies_raw.json()["total"]}')
    log(f'more: {vacancies_raw.json()["more"]}')
    return vacancies_on_page


def define_oldest_vacancy_timestamp(vacancies_all: List[Dict]) -> int:
    return min([vacancy['date_published'] for vacancy in vacancies_all])


def get_job_description(vacancy):
    vacancy_description = []
    for el in ('work', 'candidat', 'compensation'):
        if vacancy[el]:
            vacancy_description.append(str(vacancy[el]))
    return ' '.join(vacancy_description)


def get_first_metro_station(vacancy):
    if vacancy['metro']:
        return vacancy['metro'][0]['title']
    else:
        return None
