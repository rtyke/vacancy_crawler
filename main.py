from scriber import mes
from scrape_superjob import get_all_vacancies_from_to
# from data_handling_json import save_to_json, grab_newest_file_content
from data_handling_orm import get_newest_timestamp, put_vacancy_to_db
from utils import get_unixtime_several_days_back, get_unixtime_several_mins_back

from orm import Base, engine, Session


# def first_launch():
#     """for saving to json"""
#     for vacancy_chunk in get_last_month_vacancies():
#         for vacancy in vacancy_chunk:
#             save_to_json(vacancy)


# def update_vacancies():
#     """
#     For JSON.
#     Use this function only if you've downloaded vacancy data already and you
#     need update.
#     """
#     from_date = define_oldest_vacancy_timestamp(grab_newest_file_content())
#     vacancies_new = scrape_new_vacancies(from_date=from_date)
#     if not vacancies_new:
#         return f'No vacancies for date {from_date}'
#     else:
#         for vacancy in vacancies_new:
#             save_to_json(vacancy)


def first_launch():
    """for saving to db"""
    Base.metadata.create_all(bind=engine)
    session = Session()
    from_date = get_unixtime_several_days_back(days=10)
    until_date = get_unixtime_several_mins_back(minutes=10)
    for vacancy_chunk in get_all_vacancies_from_to(from_date, until_date):
        for vacancy in vacancy_chunk:
            put_vacancy_to_db(session, vacancy)
        break  #TODO dele this
    session.commit()
    session.close()


def update_vacancies():
    """
    For DATABASE.
    Use this function only if you've downloaded vacancy data already and you
    need update.
    """
    session = Session()
    from_date = get_newest_timestamp()
    until_date = get_unixtime_several_mins_back(minutes=10)
    for vacancy_chunk in get_all_vacancies_from_to(from_date, until_date):
        for vacancy in vacancy_chunk:
            put_vacancy_to_db(session, vacancy)



if __name__ == '__main__':
    first_launch()
    mes('FINISHED\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
