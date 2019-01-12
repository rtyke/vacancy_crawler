from flask import Flask, render_template

from webapp.models import Vacancy, db_session
from webapp.utils import strtime_from_unixtime


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

    @app.route('/')
    def index():
        page_title = 'Scraped Vacancies'
        vacancies_last = db_session.query(Vacancy).order_by(Vacancy.published_date.desc()).limit(10)
        return render_template(
            'index.html',
            title=page_title,
            vacancies=vacancies_last,
            convert_unixtime=strtime_from_unixtime,
        )

    return app