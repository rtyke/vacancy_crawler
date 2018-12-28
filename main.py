import os
import sys

from scriber import log
from scrape_superjob import request_vacancies_page, parse_vacancies, define_oldest_vacancy_timestamp
from data_handling_orm import create_dbase, get_oldest_timestamp, get_newest_timestamp, put_vacancy_to_db
from utils import get_unixtime_several_days_back, get_unixtime_several_mins_back, strtime_from_unixtime

from orm import Session


def define_time_period(session):
    if os.environ['RUN'] == 'new':
        period_start = get_unixtime_several_days_back(days=2)
        period_end = get_unixtime_several_mins_back(minutes=2)
    elif os.environ['RUN'] == 'update':
        period_start = get_newest_timestamp(session)
        period_end = get_unixtime_several_mins_back(minutes=2)
    else:
        return None, None
    return period_start, period_end


def main():
    session = Session()
    scrape_since, scrape_until = define_time_period(session)
    if not scrape_since:
        sys.exit('Please specify type of scrapping in RUN key: "new" or "update"')
    create_dbase()
    while True:
        vacancies_raw = request_vacancies_page(scrape_since, scrape_until)
        if not vacancies_raw:
            sys.exit('Connection error')
        vacancies_parsed = parse_vacancies(vacancies_raw)
        if not vacancies_parsed:
            log('FINISHED\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
            break
        log(f'Change upper date  {strtime_from_unixtime(scrape_until)} to:')
        scrape_until = define_oldest_vacancy_timestamp(vacancies_parsed)
        for vacancy in vacancies_parsed:
            put_vacancy_to_db(session, vacancy)
        session.commit()
    session.close()


if __name__ == '__main__':
    main()

