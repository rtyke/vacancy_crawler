from orm import session, Vacancy
from scrape_hh import generator_hh_vacancies
from convert_hh_to_orm import convert_vacancy_to_orm
from sqlalchemy import exists
from filing_db import specialization_id_hh
from datetime import datetime


def update_vacancy(specialization_id_hh):
    last_time = Vacancy.query.order_by('added_to_db_at').first().added_to_db_at
    for spec_id in specialization_id_hh:
        for vacancy in generator_hh_vacancies(last_time, datetime.now(), spec_id):
            if not session.query(exists().where(Vacancy.id_on_site == vacancy['id'])).scalar():
                convert_vacancy_to_orm(vacancy, spec_id)


# update_vacancy(specialization_id_hh)
