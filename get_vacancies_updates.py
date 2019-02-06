from celery import Celery
from celery.schedules import crontab

from webapp import create_app
from webapp.gather_resumes_sj import gather_resumes


flask_app = create_app()
celery_app = Celery('get_vacancies_updates', broker='pyamqp://guest@localhost//')


@celery_app.task
def update_resumes_one_field_sj(job_field):
    with flask_app.app_context():
        gather_resumes(run='update', job_field=job_field)


@celery_app.task
def update_resume_all_fields_sj():
    for sj_job_field_id in [33, 136, 381, 284, 100, 234, 11, 76]:
        update_resumes_one_field_sj.delay(sj_job_field_id)


@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(minute='*/2'), update_resume_all_fields_sj.s())


