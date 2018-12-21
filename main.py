import json

from scrape_superjob import scrape_new_vacancies, get_oldest_date
from orm import Base, Vacancy, engine, Session


def get_fresh():
    from_date = get_oldest_date()
    vacancies_all = scrape_new_vacancies(from_date)
    if not vacancies_all:
        print(f'No vacancies for date {from_date}')
    else:
        for vacancy in vacancies_all:
            yield vacancy


def get_job_description(vacancy):
    description = ''
    for vacancy_detail in ('work', 'candidat', 'compensation'):
        if vacancy[vacancy_detail]:
            description += vacancy[vacancy_detail] + '\n'
    return description


def get_experience(vacancy):
    if vacancy['experience']:
        return vacancy['experience']['title']
    else:
        return None


def get_metro(vacancy):
    if vacancy['metro']:
        return vacancy['metro'][0]['title']
    else:
        return None



def main():
    Base.metadata.create_all(bind=engine)
    session = Session()
    for vacancy_new in get_fresh():
        print(vacancy_new['id'])
        print(json.dumps(vacancy_new, indent=4, ensure_ascii=False))
        print(vacancy_new.keys())
        print(vacancy_new['experience'])
        salary=1000000  #TODO this!
        vacancy_in_db = Vacancy(
            id=vacancy_new['id'],
            title=vacancy_new['profession'],
            unixtime=vacancy_new['date_published'],
            description=get_job_description(vacancy_new),
            address=vacancy_new['address'],
            metro=get_metro(vacancy_new),
            type_of_work=vacancy_new['type_of_work']['title'],
            experience=get_experience(vacancy_new),
            salary=salary,
            specializations=json.dumps(vacancy_new['catalogues'], ensure_ascii=False),  #TODO discuss this
            is_archive=vacancy_new['is_archive']
        )
        session.add(vacancy_in_db)
    #
    session.commit()
    session.close()



if __name__ == '__main__':
    main()