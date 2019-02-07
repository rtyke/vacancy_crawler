from datetime import datetime

from sqlalchemy import exists

from webapp.models import db_session, Vacancy
from webapp.scrape_hh import generator_hh_vacancies
from webapp.convert_hh_to_orm import convert_vacancy_to_orm


def update_vacancies_for_field_hh(field_id):
    # TODO rewrite to get only HH vacancies
    last_time = Vacancy.query.order_by(Vacancy.added_to_db_at.desc()).first().added_to_db_at
    for vacancy in generator_hh_vacancies(
            start_time=last_time,
            end_time=datetime.now(),
            specialization_id=field_id
    ):
        if not db_session.query(exists().where(Vacancy.id_on_site == vacancy['id'])).scalar():
            db_session(convert_vacancy_to_orm(vacancy, field_id))
            db_session.commit()
