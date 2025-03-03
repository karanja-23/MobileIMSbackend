from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin

db=SQLAlchemy()



class Scanned(db.Model, SerializerMixin):
    __tablename__ = 'scanned'
    
    id = db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(80), unique=False, nullable=False)
    status=db.Column(db.String(80), default='pending', unique=False, nullable=False)
    scanned_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    
      
    def __repr__(self):
        return '<Scanned %r>' % self.id



class Request(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(50), default='pending')
    requested_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    returned_at = db.Column(db.DateTime, nullable=True)

