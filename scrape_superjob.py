import json
from typing import Dict, List
import os

import requests

from scriber import mes
from utils import get_unixtime_month_back, get_unixtime_several_mins_back, from_unixtime_to_strtime as convert


SECRET_KEY = os.environ['KEY']

HEADERS = {'X-Api-App-Id': SECRET_KEY}


def request_page_with_vacancies(from_date: int, until_date: int, page=0):
    vacancies_url = 'https://api.superjob.ru/2.0/vacancies/'
    params = {
        'count': 100,
        'page': page,
        'date_published_from': from_date,
        'date_published_to': until_date,
    }
    try:
        response = requests.get(vacancies_url, headers=HEADERS, params=params)
        response.raise_for_status()
        return response
    except requests.RequestException:
        mes('Connection error')
        return False


def scrape_vacancies(from_date: int, until_date: int):
    page_with_vacancies = request_page_with_vacancies(from_date, until_date)
    if page_with_vacancies:
        vacancies_on_page = page_with_vacancies.json().get('objects')
        mes(f'total: {page_with_vacancies.json()["total"]}')
        mes(f'more: {page_with_vacancies.json()["more"]}')
        if not vacancies_on_page:
            return False
        return vacancies_on_page
    mes('Connections issues')
    return False  # return False in case of bad internet connection


def define_oldest_vacancy_timestamp(vacancies_all: List[Dict]) -> int:
    return min([vacancy['date_published'] for vacancy in vacancies_all])


def get_job_description(vacancy):
    vacancy_detail = []
    for el in ('work', 'candidat', 'compensation'):
        if vacancy[el]:
            vacancy_detail.append(vacancy[el])
    return ' '.join(vacancy_detail)


def get_last_month_vacancies(offset=get_unixtime_several_mins_back(10)):
    month_back = get_unixtime_month_back()
    get_all_vacancies_from_to(from_date=month_back, until_date=offset)


def get_all_vacancies_from_to(from_date, until_date):
    while True:
        mes(f'Getting vacancies FROM: {convert(from_date)} TO:{convert(until_date)}')
        vacancies_chunk = scrape_vacancies(from_date, until_date)
        if vacancies_chunk:
            until_date = define_oldest_vacancy_timestamp(vacancies_chunk)
            yield vacancies_chunk
        else:
            break


def get_vacancy_by_id(id):
    """
    Doesn't work properly because of vague SuperJob API
    """
    url = 'https://api.superjob.ru/2.0/vacancies/'
    params = {'id_vacancy': id}
    response = requests.get(url, headers=HEADERS, params=params)
    print(json.dumps(response.json(), indent=4, ensure_ascii=False))

