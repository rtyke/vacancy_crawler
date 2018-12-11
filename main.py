from typing import Dict, List

import requests
import sys
import json
import time
import os

SECRET_KEY = os.environ['KEY']

HEADERS = {'X-Api-App-Id': SECRET_KEY}


def request_page_with_vacancies(page_number=0):
    vacancies_url = 'https://api.superjob.ru/2.0/vacancies/'
    params = {'count': 100, 'page': page_number}
    response = requests.get(vacancies_url, headers=HEADERS, params=params)
    if response.status_code != 200:
        return False
    else:
        return response


def extract_vacancies_from_response_data(response_data) -> List[Dict]:
    vacancies_attrs = response_data.json()['objects']
    return vacancies_attrs


def scrape_vacancies(page_number):
    vacancies_response = request_page_with_vacancies(page_number=page_number)
    if not vacancies_response:
        raise Exception('Failed connection')
    vacancies = extract_vacancies_from_response_data(vacancies_response)
    return vacancies


def save_to_json(data: List[Dict]) -> None:
    json_name = '{}.json'.format(time.time())
    with open(json_name, 'w') as fo:
        json.dump(data, fo, ensure_ascii=False)


if __name__ == '__main__':
    page_counter = 0
    while page_counter < 6:
        try:
            vacancies_attrs = scrape_vacancies(page_number=page_counter)
        except Exception:
            sys.exit('Failed connection')
        else:
            page_counter += 1
            if vacancies_attrs:
                save_to_json(vacancies_attrs)
            else:
                print(f'No content on page {page_counter - 1}')
