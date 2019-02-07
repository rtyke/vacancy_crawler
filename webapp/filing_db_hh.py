from datetime import datetime

from sqlalchemy import exists

from flask import current_app
from webapp.models import db_session, Vacancy
from webapp.scrape_hh import generator_hh_vacancies
from webapp.convert_hh_to_orm import convert_vacancy_to_orm
from webapp.utils import get_datetime_several_days_back


def gather_vacancies_hh(field_id):
    update_for_x_days = current_app.config['INIT_DOWNLOAD_VACANCIES_FOR_X_DAYS']
    for vacancy in generator_hh_vacancies(
            start_time=get_datetime_several_days_back(update_for_x_days),
            end_time=datetime.now(),
            specialization_id=field_id
    ):
        if not db_session.query(exists().where(Vacancy.id_on_site == vacancy['id'])).scalar():
            db_session.add(convert_vacancy_to_orm(vacancy, field_id))
            db_session.commit()
