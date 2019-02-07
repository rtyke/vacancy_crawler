import os


from webapp.api_key import SJ_KEY

basedir = os.path.abspath(os.path.dirname(__file__))

API_KEY_SJ = SJ_KEY
INIT_DOWNLOAD_VACANCIES_FOR_X_DAYS = 30
JOB_CATEGORIES_SJ = [33, 136, 381, 284, 100, 234, 11, 76]
SPECIALIZATIONS_IDS = [
    [5, 381, 'Банки, инвестиции, лизинг'],
    [3, 234, 'Маркетинг, реклама, PR'],
    [6, 76, 'Управление персоналом, тренинги'],
    [2, 11, 'Бухгалтерия'],
    [19, 284, 'Страхование'],
    [23, 100, 'Юристы'],
    [1, 33, 'Информационные технологии, интернет, телеком'],
    [13, 136, 'Медицина, фармацевтика']
]

SECRET_KEY = os.urandom(32)
# SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(basedir, "..", "test10jan.db")}'
