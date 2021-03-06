import sys

from flask import current_app
from webapp.models import Vacancy
from webapp.data_handling_orm_sj import put_vacancy_to_db
from webapp.scrape_sj import request_vacancies_page, parse_vacancies
from webapp.scriber import log
from webapp.utils import get_unixtime_several_days_back, get_unixtime_several_mins_back, unixtime_from_datetime, strtime_from_unixtime


def define_init_period(run='new'):
    period_end = get_unixtime_several_mins_back(minutes=10)
    if run == 'new':
        update_for_x_days = current_app.config['INIT_DOWNLOAD_VACANCIES_FOR_X_DAYS']
        period_start = get_unixtime_several_days_back(days=update_for_x_days)
    elif run == 'update':
        latest_time = Vacancy.query.order_by(Vacancy.added_to_db_at.desc()).filter(Vacancy.source == 'SuperJob').first().added_to_db_at
        period_start = unixtime_from_datetime(latest_time)
    else:
        return None
    return period_start, period_end


def define_oldest_vacancy_unixtime(vacancies_all):
    return min([vacancy['date_published'] for vacancy in vacancies_all])


def slide_period(scraping_period, vacancies):
    """Move upper period boundary to the value equal to the timestamp of the
    last found vacancy."""
    if not vacancies:  # for cases when key 'total' = 0
        return None
    period_start, period_end = scraping_period
    log(f'Change upper date {strtime_from_unixtime(period_end)}')
    period_end = define_oldest_vacancy_unixtime(vacancies)
    return period_start, period_end


def is_more_vacancies_to_scrape(vacancies_raw):
    """Check value of key more in dictionary with vacancy attributes.
    Key more is True when it's possible to make another request and fetch
    vacancies, and False when it's not possible."""
    return vacancies_raw.json()['more']


def gather_vacancies_sj(run, job_field):
    scraping_period = define_init_period(run)
    if not scraping_period:
        sys.exit('Please specify type of scrapping in RUN key: "new" or "update"')
    vacancies_more = True
    while vacancies_more:
        vacancies_raw = request_vacancies_page(scraping_period, job_field)
        if not vacancies_raw:
            sys.exit('Connection error')
        vacancies_more = is_more_vacancies_to_scrape(vacancies_raw)
        vacancies_parsed = parse_vacancies(vacancies_raw)
        scraping_period = slide_period(scraping_period, vacancies_parsed)
        for vacancy in vacancies_parsed:
            put_vacancy_to_db(vacancy)
