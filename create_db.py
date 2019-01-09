from webapp import create_app
from webapp.database import init_db

app = create_app()

with app.app_context():
    init_db()
