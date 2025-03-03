from app import app
from models import db
from sqlalchemy import text

with app.app_context():
    db.session.execute(text("DROP TABLE alembic_version;"))
    db.session.commit()