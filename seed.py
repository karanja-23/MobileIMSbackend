from app import app
from models import db
from sqlalchemy import text, inspect

with app.app_context():
    # Get the current database engine
    inspector = inspect(db.engine)
    
    # Check if the 'Request' table exists
    if 'request' in inspector.get_table_names():
        # Create a connection and execute the SQL to alter the table
        with db.engine.connect() as connection:
            # Add new columns to the 'request' table
            connection.execute(text("""
                ALTER TABLE request
                ADD COLUMN asset_id INTEGER NOT NULL,
                ADD COLUMN user_name VARCHAR(100) NOT NULL,
                ADD COLUMN asset_name VARCHAR(100) NOT NULL,
                ADD COLUMN user_id INTEGER NOT NULL;
            """))
            print("Request table altered successfully")
    else:
        print("Request table does not exist")
        