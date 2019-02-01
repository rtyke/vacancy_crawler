from flask import Flask, render_template, flash, redirect, url_for

from webapp.models import Vacancy, db_session
from webapp.data_handling_orm import search_vacancies_by_word
from webapp.search_forms import SearchForm
from webapp.utils import strtime_from_unixtime


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

    @app.route('/')
    def index():
        search_form = SearchForm()
        page_title = 'Scraped Vacancies'
        vacancies_last = db_session.query(Vacancy).order_by(Vacancy.published_date.desc()).limit(10)
        return render_template(
            'index.html',
            title=page_title,
            vacancies=vacancies_last,
            convert_unixtime=strtime_from_unixtime,
            search_form=search_form
        )

    @app.route('/search', methods=['POST'])
    def search():
        title = 'Поиск вакансий'
        search_form = SearchForm()
        # TODO validate_on_submit() ???
        search_word = search_form.search.data
        vacancies_searched = search_vacancies_by_word(search_word)
        return render_template(
            'search_results.html',
            page_title=title,
            vacancies=vacancies_searched,
            search_form=search_form,
            search_word=search_word,
            convert_unixtime=strtime_from_unixtime
        )

    return app

