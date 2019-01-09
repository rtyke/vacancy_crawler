import os
import sys

from scriber import log
from scrape_superjob import request_vacancies_page, parse_vacancies, define_oldest_vacancy_timestamp
from data_handling_orm import create_dbase, get_newest_timestamp, put_vacancy_to_db
from utils import get_unixtime_several_days_back, get_unixtime_several_mins_back, strtime_from_unixtime

from orm import Session


def define_init_period(session):
    if os.environ['RUN'] == 'new':
        period_start = get_unixtime_several_days_back(days=20)
        period_end = get_unixtime_several_mins_back(minutes=10)
    elif os.environ['RUN'] == 'update':
        period_start = get_newest_timestamp(session)
        period_end = get_unixtime_several_mins_back(minutes=10)
    else:
        return None
    return period_start, period_end


def slide_period(scraping_period, vacancies):
    """Move upper period boundary to the value equal to the timestamp of the
    last found vacancy."""
    if not vacancies:  # for cases when key 'total' = 0
        return None
    period_start, period_end = scraping_period
    log(f'Change upper date  {strtime_from_unixtime(period_end)}')
    period_end = define_oldest_vacancy_timestamp(vacancies)
    return period_start, period_end


def is_more_vacancies_to_scrape(vacancies_raw):
    """Check value of key more in dictionary with vacancy attributes.
    Key more is True when it's possible to make another request and fetch
    vacancies, and False when it's not possible."""
    return vacancies_raw.json()['more']


def main():
    session = Session()
    scraping_period = define_init_period(session)
    if not scraping_period:
        sys.exit('Please specify type of scrapping in RUN key: "new" or "update"')
    create_dbase()
    vacancies_more = True
    while vacancies_more:
        vacancies_raw = request_vacancies_page(scraping_period)
        if not vacancies_raw:
            sys.exit('Connection error')
        vacancies_more = is_more_vacancies_to_scrape(vacancies_raw)
        vacancies_parsed = parse_vacancies(vacancies_raw)
        scraping_period = slide_period(scraping_period, vacancies_parsed)
        for vacancy in vacancies_parsed:
            put_vacancy_to_db(session, vacancy)
    session.close()


if __name__ == '__main__':
    main()
    log('FINISHED\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')

