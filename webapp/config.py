import os
from webapp.api_key import SJ_KEY

basedir = os.path.abspath(os.path.dirname(__file__))

SJ_API_KEY = SJ_KEY
# SQLALCHEMY_DATABASE_уURI = f'sqlite:///{os.path.join(basedir, "..", "vacancies_sj.db")}'