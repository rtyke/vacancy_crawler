from datetime import datetime
from orm import session, Vacancy, Field


def get_vacancy_address(vacancy):
    try:
        return ', '.join([vacancy[key] for key in ['city', 'street', 'building']])
    except KeyError:
        return


def get_metro_station_from_address(address):
    try:
        return address['metro'].get('station_name')
    except (TypeError, AttributeError):
        return None


def convert_vacancy_to_orm(vacancy, spec_id):
    vacancy_orm = Vacancy(
           id_on_site=vacancy['id'],
           title=vacancy['name'],
           published_date=vacancy['published_at'],
           description=vacancy['snippet']['responsibility'],
           salary_from=vacancy['salary'].get('from') if vacancy['salary'] is not None else None,
           salary_to=vacancy['salary'].get('to') if vacancy['salary'] is not None else None,
           currency=vacancy['salary']['currency'] if vacancy['salary'] is not None else None,
           firm=vacancy['employer']['name'],
           address=get_vacancy_address(vacancy),
           town=vacancy['address']['city'] if vacancy['address'] is not None else None,
           metro=get_metro_station_from_address(vacancy['address']),
           type_of_work=None,
           experience=None,
           is_archive=vacancy['archived'],
           added_to_db_at=datetime.now().isoformat(),
           url=vacancy['alternate_url']
          )
    vacancy_orm.field = [Field.query.filter_by(id_hh=spec_id).first()]
    return vacancy_orm


