from webapp import create_app
from webapp.models import init_db

app = create_app()

with app.app_context():
    init_db()
