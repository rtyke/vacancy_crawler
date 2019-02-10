from sqlalchemy import or_, func

from webapp.models import Vacancy


def print_vacancies_on_page(page, vacancies_per_page=10):
    start = vacancies_per_page*(page-1)
    end = vacancies_per_page*page
    print(start, end, end-start)
    return Vacancy.query.order_by(Vacancy.published_date.desc()).slice(start, end)


def search_by_word(pattern):
    title_match = Vacancy.title.ilike(pattern)
    description_match = Vacancy.description.ilike(pattern)
    return Vacancy.query.filter(or_(title_match, description_match))


def search_by_word_city(pattern, city):
    # TODO doesn't work properly
    title_match = Vacancy.title.ilike(pattern)
    description_match = Vacancy.description.ilike(pattern)
    city_match = func.lower(Vacancy.town) == city.lower()
    return Vacancy.query.filter(or_(title_match, description_match), city_match)


def search_by_city(city):
    city_match = func.lower(Vacancy.town) == city.lower()
    return Vacancy.query.filter(city_match)


def search_vacancies(word, city, spec):
    pattern = f'%{str.lower(word)}%'
    # TODO add exceptions
    if word:
        return search_by_word(pattern)
    elif word and city:
        return search_by_word_city(pattern, city)
    elif city:
        return search_by_city(city)
