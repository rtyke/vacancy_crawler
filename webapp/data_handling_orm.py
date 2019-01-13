import json
import time

from webapp.models import Vacancy, Salary, db_session


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
            specializations=json.dumps(vacancy['catalogues'], ensure_ascii=False),  # TODO discuss this
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
        db_session.add(vacancy_orm)
        db_session.add(salary_orm)
        db_session.commit()
