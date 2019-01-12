import os
from webapp.api_key import SJ_KEY

basedir = os.path.abspath(os.path.dirname(__file__))

SJ_API_KEY = SJ_KEY
INIT_DOWNLOAD_VACANCIES_FOR_X_DAYS = 1
# SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(basedir, "..", "test10jan.db")}'
