from datetime import datetime

from sqlalchemy import exists

from webapp.models import db_session, Vacancy
from webapp.scrape_hh import generator_hh_vacancies, get_datetime_month_ago
from webapp.convert_hh_to_orm import convert_vacancy_to_orm


def gather_vacancies_hh(field_id):
    for vacancy in generator_hh_vacancies(get_datetime_month_ago(), datetime.now(), field_id):
        if not db_session.query(exists().where(Vacancy.id_on_site == vacancy['id'])).scalar():
            db_session.add(convert_vacancy_to_orm(vacancy, field_id))
            db_session.commit()
