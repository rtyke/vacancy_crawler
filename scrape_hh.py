import requests
import json
from typing import Dict
from datetime import date, datetime, timedelta


URL = 'https://api.hh.ru/vacancies/'
HEADERS = {'User-Agent': 'api-test-agent'}


def get_datetime_month_ago():
    today = datetime.now()
    current_day = today.day
    last_month = (today.replace(day=1) -
                  timedelta(days=1)).replace(day=current_day)
    return last_month


def generator_hh_vacancies_last_month() -> Dict:
    global URL, HEADERS
    start_time = get_datetime_month_ago()
    end_time = datetime.now()
    while start_time < end_time:
        interval_end = start_time + timedelta(days=1)
        params = {'page': 0,
                  'per_page': 100,
                  'date_from': datetime.strftime(start_time, "%Y-%m-%dT%H:%M:%S"),
                  'date_to': datetime.strftime(interval_end, "%Y-%m-%dT%H:%M:%S")}
        # print(start_time, interval_end, sep=' ======> ')
        while params['page'] < 20:
            response = requests.get(url=URL, params=params, headers=HEADERS)
            params['page'] += 1
            yield from response.json()['items']
        start_time = interval_end + timedelta(minutes=5)


def pretty_print_json(data: Dict):
    print(json.dumps(data, indent=4, sort_keys=False, ensure_ascii=False))


def main():
    result = []
    for vacancy in generator_hh_vacancies_last_month():
        result.append(vacancy['id'])
    print(len(result), len(set(result)))


if __name__ == '__main__':
    main()
