from typing import Dict, List
import requests
import os

SECRET_KEY = os.environ['KEY']

HEADERS = {'X-Api-App-Id': SECRET_KEY}


def request_page_with_vacancies(since_date: int, page_number: int):
    vacancies_url = 'https://api.superjob.ru/2.0/vacancies/'
    params = {
        'count': 100,
        'page': page_number,
        'date_published_from': since_date
    }
    try:
        response = requests.get(vacancies_url, headers=HEADERS, params=params)
        response.raise_for_status()
        return response
    except requests.RequestException:
        print('Connection error')
        return False


def scrape_vacancies(since_date: int) -> List[Dict]:
    vacancies_all = []
    for page_number in range(6):
        response = request_page_with_vacancies(
            since_date=since_date,
            page_number=page_number,
        )
        if response:
            vacancies_on_page = response.json().get('objects', [])
            vacancies_all.extend(vacancies_on_page)
    return vacancies_all


def main():
    vacancies_all = scrape_vacancies(since_date=1544630400)
    if not vacancies_all:
        print('No vacancies for date 1544630400')
    else:
        for vacancy in vacancies_all:
            print(vacancy)


if __name__ == '__main__':
    main()
