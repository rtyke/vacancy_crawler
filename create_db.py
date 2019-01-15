from webapp import create_app
from webapp.models import init_db
from webapp.models import fill_in_fields_handbook

app = create_app()

with app.app_context():
    init_db()
    fill_in_fields_handbook()
