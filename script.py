from app import app
from models import db
from sqlalchemy import inspect

# Ensure we are in an application context
with app.app_context():
    # Get the inspector for the database
    inspector = inspect(db.engine)

    # Get the list of all table names in the database
    tables = inspector.get_table_names()

    # Check if 'requests' table exists in the database
    if 'request' in tables:
        print("The 'request' table exists.")
    else:
        print("The 'requests' table does not exist.")
