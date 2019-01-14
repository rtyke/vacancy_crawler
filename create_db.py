from webapp import create_app
from webapp.models import init_db
from webapp.models import add_specializations

app = create_app()

with app.app_context():
    init_db()
    add_specializations()
