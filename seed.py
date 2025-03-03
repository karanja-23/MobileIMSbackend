from app import app
from models import Scanned,db

with app.app_context():
    Scanned.query.delete()
    
    db.session.commit()