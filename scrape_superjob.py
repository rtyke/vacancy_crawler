from typing import Dict, List
import os

import requests

from scriber import log
from utils import strtime_from_unixtime


# SECRET_KEY = os.environ['KEY']
SECRET_KEY = 'v1.r07af662aed8eb82c8ce492dc02187f2c175d3fe0bf2bce65f7ac1928428ff0b4046f3a48.d926539b8ea9ba66a2181b41fedfaf0c6ded2e83'

HEADERS = {'X-Api-App-Id': SECRET_KEY}


def request_vacancies_page(from_date: int, until_date: int):
    log(f'Get vacancies till {strtime_from_unixtime(until_date)} since {strtime_from_unixtime(from_date)}')
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
