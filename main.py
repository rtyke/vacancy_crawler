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


def scrape_vacancies():
    for page_number in range(6):
        vacancies_response = request_page_with_vacancies(page_number=page_number)
        if not vacancies_response:
            raise Exception('Failed connection')
        yield extract_vacancies_from_response_data(vacancies_response)


def save_to_json(data: List[Dict]) -> None:
    json_name = '{}.json'.format(time.time())
    with open(json_name, 'w') as fo:
        json.dump(data, fo, ensure_ascii=False)


def main():
    try:
        for vacancy_page in scrape_vacancies():
            if vacancy_page:
                save_to_json(vacancy_page)
            else:
                # TODO get page number. Does generator have attributes?
                print(f'No content on page')
    except Exception:
        sys.exit('Failed connection')


if __name__ == '__main__':
    main()
