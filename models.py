from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin

db=SQLAlchemy()

class Asset(db.Model, SerializerMixin):
    __tablename__ = 'assets'
    
    id = db.Column(db.Integer, primary_key=True)
    asset_id = db.Column(db.BigInteger, unique=True, nullable=False)
    name = db.Column(db.String(80), unique=False, nullable=False)
    description = db.Column(db.String(225), unique=False, nullable=False)
    condition = db.Column(db.String(80), unique=False, nullable=False)
    category = db.Column(db.String(80), unique=False, nullable=False)
    space=db.Column(db.String(80), unique=False, nullable=False)
    status=db.Column(db.String(80), unique=False, nullable=False)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)
    
    def __repr__(self):
        return '<Asset %r>' % self.name


   
class User(db.Model, SerializerMixin):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=True)
    phone_number = db.Column(db.String(80), unique=False, nullable=True)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    
    scanned = db.relationship('Scanned', lazy=True)
    
    def __repr__(self):
        return '<User %r>' % self.username



class Scanned(db.Model, SerializerMixin):
    __tablename__ = 'scanned'
    
    id = db.Column(db.Integer, primary_key=True)
    asset_id = db.Column(db.Integer, db.ForeignKey('assets.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    scanned_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    
    asset = db.relationship('Asset', backref=db.backref('scanned', lazy=True))
    user = db.relationship('User', backref=db.backref('scanned_items', lazy=True))
    
    serialize_rules = ('-asset', '-user')   
    def __repr__(self):
        return '<Scanned %r>' % self.id