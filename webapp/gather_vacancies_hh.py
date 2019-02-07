from datetime import datetime

from sqlalchemy import exists

from flask import current_app
from webapp.models import db_session, Vacancy
from webapp.scrape_hh import generator_hh_vacancies
from webapp.convert_hh_to_orm import convert_vacancy_to_orm
from webapp.utils import get_datetime_several_days_back


def define_scrapping_period(run):
    period_end = datetime.now()
    if run == 'new':
        update_for_x_days = current_app.config['INIT_DOWNLOAD_VACANCIES_FOR_X_DAYS']
        period_start = get_datetime_several_days_back(days=update_for_x_days)
    elif run == 'update':
        # TODO rewrite to get only HH vacancies
        # latest_time = Vacancy.query.order_by(Vacancy.added_to_db_at.desc()).first().added_to_db_at
        latest_time = Vacancy.query.order_by(Vacancy.added_to_db_at.desc()).filter(Vacancy.source == 'HeadHunter').first().added_to_db_at
        period_start = latest_time
    else:
        return None
    return period_start, period_end


def gather_vacancies_hh(run, job_field):
    start_time, end_time = define_scrapping_period(run)
    for vacancy in generator_hh_vacancies(
            start_time=start_time,
            end_time=end_time,
            specialization_id=job_field
    ):
        if not db_session.query(exists().where(Vacancy.id_on_site == vacancy['id'])).scalar():
            db_session.add(convert_vacancy_to_orm(vacancy, job_field))
            db_session.commit()
