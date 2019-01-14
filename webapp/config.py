import os
from webapp.api_key import SJ_KEY

basedir = os.path.abspath(os.path.dirname(__file__))

API_KEY_SJ = SJ_KEY
INIT_DOWNLOAD_VACANCIES_FOR_X_DAYS = 1
JOB_CATEGORIES_SJ = [33, 136, 381, 284, 100, 234, 11, 76]
# SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(basedir, "..", "test10jan.db")}'
