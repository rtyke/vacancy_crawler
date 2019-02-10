from flask import Flask, render_template

from webapp.models import Vacancy, session
from webapp.search_queries import search_vacancies, print_vacancies_on_page
from webapp.search_forms import SmallSearchForm, SearchForm
from webapp.utils import strtime_from_unixtime


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        session.remove()

    @app.route('/')
    def index():
        # TODO add redirect to page/1
        search = SearchForm()
        page_title = 'Новые вакансии'
        vacancies_last = Vacancy.query.order_by(Vacancy.published_date.desc()).limit(10)
        return render_template(
            'index.html',
            title=page_title,
            vacancies=vacancies_last,
            search_form=search,
        )


    @app.route('/page/<page_number>')
    def pagination(page_number):
        # TODO add 404 error for pages out of range
        page_number = int(page_number)
        search = SearchForm()
        page_title = 'Новые вакансии'
        vacancies_on_page = print_vacancies_on_page(page=page_number)
        return render_template(
            'index.html',
            title=page_title,
            vacancies=vacancies_on_page,
            search_form=search,
            pages=range(1, 15)
        )


    @app.route('/search', methods=['POST'])
    def search():
        title = 'Поиск вакансий'
        search = SearchForm()
        vacancies_searched = search_vacancies(
            search.search.data,
            search.city.data,
            search.spec.data
        )
        return render_template(
            'index.html',
            page_title=title,
            vacancies=vacancies_searched,
            search_form=search,
        )

    return app

