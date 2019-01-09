from webapp import create_app
from webapp.gather_resumes_sj import gather_resumes


app = create_app()

with app.app_context():
    gather_resumes(run='update')
