import json
import time

from orm import Vacancy, Session, engine, Base
from scrape_superjob import get_job_description


def create_dbase():
    Base.metadata.create_all(bind=engine)


def get_newest_timestamp(session):
    timestamps = session.query(Vacancy.unixtime).all()
    return str(max(timestamps)[0])


def put_vacancy_to_db(session, vacancy):
    vacancy_orm = Vacancy(
        vid=vacancy['id'],
        title=vacancy['profession'],
        unixtime=vacancy['date_published'],
        description=get_job_description(vacancy),
        address=vacancy['address'],
        metro=json.dumps(vacancy['metro'], ensure_ascii=False),
        type_of_work=vacancy['type_of_work']['title'],
        experience=vacancy['experience']['title'],
        salary=1000000,  # TODO discuss this
        specializations=json.dumps(vacancy['catalogues'], ensure_ascii=False),  # TODO discuss this
        is_archive=vacancy['is_archive'],
        update_time=int(time.time()),
    )
    session.add(vacancy_orm)
    session.commit()






