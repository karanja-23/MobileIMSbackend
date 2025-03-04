from app import app
from models import db
from sqlalchemy import text  # Import the text() function

# Make sure we are in an application context
with app.app_context():
    # Step 1: Create the sequence if it doesn't exist
    db.session.execute(text('''
        CREATE SEQUENCE IF NOT EXISTS scanned_id_seq
        START WITH 1
        INCREMENT BY 1
        NO MINVALUE
        NO MAXVALUE
        CACHE 1;
    '''))

    # Step 2: Alter the 'id' column to use the sequence
    db.session.execute(text('''
        ALTER TABLE scanned
        ALTER COLUMN id SET DEFAULT nextval('scanned_id_seq');
    '''))

    # Commit the transaction to save changes
    db.session.commit()

    # Optionally, check if the table structure was updated
    result = db.session.execute(text("SELECT column_name FROM information_schema.columns WHERE table_name='scanned';"))
    for row in result:
        print(row)
