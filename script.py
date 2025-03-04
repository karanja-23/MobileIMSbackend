from app import app
from models import db, Request  # Make sure your model is defined properly
from sqlalchemy.orm import sessionmaker

# Create a session
Session = sessionmaker(bind=db.engine)
session = Session()

with app.app_context():
    # Example of querying all requests
    all_requests = session.query(Request).all()
    
    for request in all_requests:
        print(f"Request ID: {request.id}, Status: {request.status}")

    # Example of adding a new request
    new_request = Request(
        status="pending",
        asset_id=1,
        user_name="Hosea",
        asset_name="Lenovo ideapad",
        user_id=7
    )
    
    session.add(new_request)
    session.commit()
    print("New request added!")

    # Close the session
    session.close()
