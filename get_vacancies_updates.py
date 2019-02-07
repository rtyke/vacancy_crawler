from celery import Celery
from celery.schedules import crontab

from webapp import create_app
from webapp.gather_vacancies_sj import gather_vacancies_sj
from webapp.update_vacancies_hh import update_vacancies_for_field_hh


flask_app = create_app()
celery_app = Celery('get_vacancies_updates', broker='pyamqp://guest@localhost//')


@celery_app.task
def update_vacancies_one_field(job_field_ids):
    with flask_app.app_context():
        update_vacancies_for_field_hh(job_field_ids[0])
        gather_vacancies_sj(run='update', job_field=job_field_ids[1])


@celery_app.task
def update_vacancies_all_fields():
    hh_sj_field_ids = [(5, 381), (3, 234), (6, 76), (2, 11), (19, 284), (23, 100), (1, 33), (13, 136)]
    for field_id in hh_sj_field_ids:
        update_vacancies_one_field.delay(field_id)


@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(minute='*/2'), update_vacancies_all_fields.s())


