import json
from datetime import datetime, timedelta

from webapp.scriber import log

import requests


HEADERS = {'User-Agent': 'api-test-agent'}


def get_hh_specialization_dict():
    global HEADERS
    response = requests.get(url='https://api.hh.ru/specializations', headers=HEADERS)
    return [dict(id=specialization['id'], name=specialization['name']) for specialization in response.json()]


def get_datetime_month_ago():
    today = datetime.now()
    current_day = today.day
    last_month = (today.replace(day=1) -
                  timedelta(days=1)).replace(day=current_day)
    return last_month


def generator_hh_vacancies(
        start_time,
        end_time,
        specialization_id,
        size_window={'hours': 6},
        between_windows={'minutes': 5}
):
    global HEADERS
    while start_time < end_time:
        interval_end = start_time + timedelta(**size_window)
        log(f'HH Get vacancies till {datetime.strftime(interval_end, "%Y-%m-%dT%H:%M:%S")} since {datetime.strftime(start_time, "%Y-%m-%dT%H:%M:%S")}')
        params = {'page': 0,
                  'per_page': 100,
                  'date_from': datetime.strftime(start_time, "%Y-%m-%dT%H:%M:%S"),
                  'date_to': datetime.strftime(interval_end, "%Y-%m-%dT%H:%M:%S"),
                  'specialization': specialization_id}
        while params['page'] < 20:
            try:
                response = requests.get(url='https://api.hh.ru/vacancies/', params=params, headers=HEADERS)
                params['page'] += 1
                yield from response.json()['items']
            except requests.exceptions.Timeout:
                continue
        start_time = interval_end + timedelta(**between_windows)


def generator_vacancy_from_specializations(
        start_time,
        end_time,
        specialization_data
):
    """
    :param specialization_data: list
    :return: vacancy - dict(), spec - dict()
    """
    for spec in get_hh_specialization_dict():
        if spec['name'] in specialization_data:
            for vacancy in generator_hh_vacancies(start_time, end_time, spec['id']):
                yield vacancy, spec


def pretty_print_json(data):
    print(json.dumps(data, indent=4, sort_keys=False, ensure_ascii=False))
