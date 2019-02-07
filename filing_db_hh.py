from webapp.models import db_session, Field, Vacancy
from scrape_hh import generator_hh_vacancies, get_datetime_month_ago
from convert_hh_to_orm import convert_vacancy_to_orm
from sqlalchemy import exists
from datetime import datetime

specialization_data = [[5, 381, 'Банки, инвестиции, лизинг'],
                       [3, 234, 'Маркетинг, реклама, PR'],
                       [6, 76, 'Управление персоналом, тренинги'],
                       [2, 11, 'Бухгалтерия'],
                       [19, 284, 'Страхование'],
                       [23, 100, 'Юристы'],
                       [1, 33, 'Информационные технологии, интернет, телеком'],
                       [13, 136, 'Медицина, фармацевтика']]

specialization_id_hh = [spec[0] for spec in specialization_data]


def filling_fileds(specialization_data):
    for data in specialization_data:
        db_session.add(Field(*data))
    db_session.commit()


def filling_vacancy(specialization_id_hh):
    for spec_id in specialization_id_hh:
        for vacancy in generator_hh_vacancies(get_datetime_month_ago(), datetime.now(), spec_id):
            if not db_session.query(exists().where(Vacancy.id_on_site == vacancy['id'])).scalar():
                db_session.add(convert_vacancy_to_orm(vacancy, spec_id))
                db_session.commit()


if __name__ == '__main__':
    # filling_fileds(specialization_data)
    filling_vacancy(specialization_id_hh)


