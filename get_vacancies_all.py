from celery import Celery

from webapp import create_app
from webapp.filing_db_hh import gather_vacancies_hh
from webapp.gather_resumes_sj import gather_vacancies_sj


flask_app = create_app()
celery_app = Celery('get_vacancies_all', broker='pyamqp://guest@localhost//')


@celery_app.task
def gather_all_vacancies_sj(job_field):
    with flask_app.app_context():
        gather_vacancies_sj(run='new', job_field=job_field)


@celery_app.task
def gather_all_vacancies_hh(job_field):
    with flask_app.app_context():
        gather_vacancies_hh(job_field)


if __name__ == '__main__':
    # TODO move to config file
    hh_sj_field_ids = [(5, 381), (3, 234), (6, 76), (2, 11), (19, 284), (23, 100), (1, 33), (13, 136)]
    for field_id in hh_sj_field_ids:
        gather_all_vacancies_hh.delay(field_id[0])
        gather_all_vacancies_sj.delay(field_id[1])
