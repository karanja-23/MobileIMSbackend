from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin

db=SQLAlchemy()

class Asset(db.Model, SerializerMixin):
    __tablename__ = 'asset'
    
    id = db.Column(db.Integer, primary_key=True)
    asset_id = db.Column(db.String(80), unique=True, nullable=False)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(80), unique=True, nullable=False)
    condition = db.Column(db.String(80), unique=True, nullable=False)
    category = db.Column(db.String(80), unique=True, nullable=False)
    space=db.Column(db.String(80), unique=True, nullable=False)
    status=db.Column(db.String(80), unique=True, nullable=False)
    
    def __repr__(self):
        return '<Asset %r>' % self.name