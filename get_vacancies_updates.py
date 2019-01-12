from webapp import create_app
from webapp.gather_resumes_sj import gather_resumes


def get_vacancies_updates():
    app = create_app()
    with app.app_context():
        gather_resumes(run='update')

get_vacancies_updates()

# app = create_app()
# with app.app_context():
#     gather_resumes(run='update')
