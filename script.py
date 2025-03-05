from app import app
from models import db
from sqlalchemy import text

# Ensure we are in an application context
with app.app_context():
    # Get the current engine
    engine = db.engine

    # Create a connection from the engine
    with engine.connect() as connection:
        # Get the columns in the user table
        result = connection.execute(text("""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name = 'user';
        """))

        # Print the columns
        for row in result:
            print(row[0])