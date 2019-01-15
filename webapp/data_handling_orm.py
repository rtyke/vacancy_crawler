import time

from flask import current_app
from webapp.models import Vacancy, Salary, db_session, Field


def get_job_description(vacancy):
    vacancy_description = []
    for el in ('work', 'candidat', 'compensation'):
        if vacancy[el]:
            vacancy_description.append(str(vacancy[el]))
    return ' '.join(vacancy_description)


def get_first_metro_station(vacancy):
    if vacancy['metro']:
        return vacancy['metro'][0]['title']
    else:
        return None


def put_vacancy_to_db(vacancy):
    if 'id' not in vacancy:
        return
    vacancy_not_in_db = Vacancy.query.filter(Vacancy.id_on_site == vacancy['id']).count() < 1
    if vacancy_not_in_db:
        vacancy_orm = Vacancy(
            id_on_site=vacancy['id'],
            title=vacancy['profession'],
            published_date=vacancy['date_published'],
            description=get_job_description(vacancy),
            firm=vacancy['firm_name'],
            address=vacancy['address'],
            town=vacancy['town']['title'],
            metro=get_first_metro_station(vacancy),
            type_of_work=vacancy['type_of_work']['title'],
            experience=vacancy['experience']['title'],
            is_archive=vacancy['is_archive'],
            added_to_db_at=int(time.time()),
            url=vacancy['link']
        )
        salary_orm = Salary(
            agreement=vacancy['agreement'],
            payment_from=vacancy['payment_from'],
            payment_to=vacancy['payment_to'],
            currency=vacancy['currency'],
            vacancy=vacancy_orm

        )
        vacancy_fields_objects = []
        for vacancy_field in vacancy['catalogues']:
            if vacancy_field['id'] in current_app.config['JOB_CATEGORIES_SJ']:
                field_obj = Field.query.filter(Field.id_sj == vacancy_field['id']).all()[0]
                vacancy_fields_objects.append(field_obj)
        vacancy_fields_objects = list(set(vacancy_fields_objects))

        vacancy_orm.field = vacancy_fields_objects

        db_session.add(vacancy_orm)
        db_session.add(salary_orm)
        db_session.commit()


