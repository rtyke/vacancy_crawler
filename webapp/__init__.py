from flask import Flask, render_template

from webapp.database import db_session
from webapp.models import Vacancy


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

    @app.route('/')
    def index():
        page_title = 'Scraped Vacancies'
        vacancies_last = db_session.query(Vacancy).order_by(Vacancy.published_date.desc())[:10]
        return render_template('index.html', title=page_title, vacancies=vacancies_last)

    return app