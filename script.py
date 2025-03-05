from app import app
from models import db
from sqlalchemy import text

# Ensure we are in an application context
with app.app_context():
    # Run raw SQL to add the 'space' column
    db.session.execute(text('ALTER TABLE orders ADD COLUMN space VARCHAR(255)'))
    db.session.commit()  # Commit the changes to the database