from datetime import datetime

from sqlalchemy import exists

from webapp.models import db_session, Vacancy
from webapp.scrape_hh import generator_hh_vacancies
from webapp.convert_hh_to_orm import convert_vacancy_to_orm


def update_vacancy(specialization_id_hh):
    # TODO depreciated
    last_time = Vacancy.query.order_by(Vacancy.added_to_db_at.desc()).first().added_to_db_at
    for spec_id in specialization_id_hh:
        for vacancy in generator_hh_vacancies(last_time, datetime.now(), spec_id):
            if not db_session.query(exists().where(Vacancy.id_on_site == vacancy['id'])).scalar():
                convert_vacancy_to_orm(vacancy, spec_id)


def update_vacancies_for_field_hh(field_id):
    # TODO rewrite to get only HH vacancies
    last_time = Vacancy.query.order_by(Vacancy.added_to_db_at.desc()).first().added_to_db_at
    for vacancy in generator_hh_vacancies(last_time, datetime.now(), field_id):
        if not db_session.query(exists().where(Vacancy.id_on_site == vacancy['id'])).scalar():
            convert_vacancy_to_orm(vacancy, field_id)
