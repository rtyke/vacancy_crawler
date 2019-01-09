import json
import time

# from webapp.models import Vacancy, Salary, Session, engine, Base
from webapp.models import Vacancy, Salary, Base
from webapp.scrape_superjob import get_job_description, get_first_metro_station


# def create_dbase():
#     Base.metadata.create_all(bind=engine)


def get_newest_timestamp(session):
    timestamps = session.query(Vacancy.published_date).all()
    return str(max(timestamps)[0])


def put_vacancy_to_db(session, vacancy):
    vacancy_not_in_db = session.query(Vacancy).filter(Vacancy.id_on_site == vacancy['id']).count() < 1
    if vacancy_not_in_db:
        vacancy_orm = Vacancy(
            id_on_site=vacancy['id'],
            title=vacancy['profession'],
            published_date=vacancy['date_published'],
            description=get_job_description(vacancy),
            address=vacancy['address'],
            # metro=json.dumps(vacancy['metro'], ensure_ascii=False),
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
        session.add(vacancy_orm)
        session.add(salary_orm)
        session.commit()






