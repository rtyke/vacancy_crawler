from celery import Celery

from webapp import create_app
from webapp.gather_resumes_sj import gather_resumes


flask_app = create_app()
celery_app = Celery('get_vacancies_all', broker='pyamqp://guest@localhost//')


@celery_app.task
def gather_resumes_sj(job_field):
    with flask_app.app_context():
        gather_resumes(run='new', job_field=job_field)


if __name__ == '__main__':
    # TODO move to
    for sj_job_field_id in [33, 136, 381, 284, 100, 234, 11, 76]:
        gather_resumes_sj.delay(sj_job_field_id)
