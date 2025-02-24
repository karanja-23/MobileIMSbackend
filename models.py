from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin

db=SQLAlchemy()

class Asset(db.Model, SerializerMixin):
    __tablename__ = 'assets'
    
    id = db.Column(db.Integer, primary_key=True)
    asset_id = db.Column(db.String(80), unique=True, nullable=False)
    name = db.Column(db.String(80), unique=False, nullable=False)
    description = db.Column(db.String(225), unique=False, nullable=False)
    condition = db.Column(db.String(80), unique=False, nullable=False)
    category = db.Column(db.String(80), unique=False, nullable=False)
    space=db.Column(db.String(80), unique=False, nullable=False)
    status=db.Column(db.String(80), unique=False, nullable=False)
    
    def __repr__(self):
        return '<Asset %r>' % self.name
    
class User(db.Model, SerializerMixin):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    
    def __repr__(self):
        return '<User %r>' % self.username