import time
from threading import Thread

from flask import Flask, render_template

from webapp.database import db_session
from webapp.models import Vacancy
from webapp.utils import strtime_from_unixtime
from webapp.gather_resumes_sj import gather_resumes
from webapp.scriber import log

from get_vacancies_updates import get_vacancies_updates


def get_updates():
    while True:
        time.sleep(1)
        log('Put updates to DB')
        get_vacancies_updates()
# def get_updates():
#     while True:
#         time.sleep(3)
#         log('LALALALLAL')
#         print('POOPOPOPOPO')

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
    updates = Thread(target=get_updates)
    updates.start()
    return app
