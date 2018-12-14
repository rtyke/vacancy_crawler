import requests
import json
from typing import Dict


URL = 'https://api.hh.ru/vacancies/'
HEADERS = {'User-Agent': 'api-test-agent'}


def get_hh_vacancies() -> Dict:
    global URL, HEADERS
    params = {'page': 0, 'per_page': 100, 'period': 30}
    while params['page'] < 20:
        response = requests.get(url=URL, params=params, headers=HEADERS)
        params['page'] += 1
        yield from response.json()['items']


def pretty_print_json(data: Dict):
    print(json.dumps(data, indent=4, sort_keys=False, ensure_ascii=False))


def main():
    for vacancy in get_hh_vacancies():
        pretty_print_json(vacancy)
        # break


if __name__ == '__main__':
    main()
