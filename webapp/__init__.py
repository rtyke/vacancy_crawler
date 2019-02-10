from flask import Flask, render_template

from webapp.models import Vacancy, session
from webapp.search_queries import search_vacancies
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
        search = SearchForm()
        page_title = 'Новые вакансии'
        vacancies_last = Vacancy.query.order_by(Vacancy.published_date.desc()).limit(10)
        return render_template(
            'index.html',
            title=page_title,
            vacancies=vacancies_last,
            search_form=search,
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

