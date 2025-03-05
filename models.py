from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin

db=SQLAlchemy()



class Scanned(db.Model, SerializerMixin):
    __tablename__ = 'scanned'
    
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False)
    name=db.Column(db.String(80), unique=False, nullable=False)
    status=db.Column(db.String(80), default='pending', unique=False, nullable=False)
    scanned_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    
    
    
    
    def __repr__(self):
        return '<Scanned %r>' % self.id



class Request(db.Model, SerializerMixin):
    
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)
    status = db.Column(db.String(50), default='pending')
    requested_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    asset_id = db.Column(db.Integer, nullable=False)
    user_name = db.Column(db.String(100), nullable=False)
    asset_name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user=db.relationship("User", back_populates="requests", foreign_keys=[user_id])
    serialize_only = ('id', 'status', 'requested_at', 'asset_id', 'user_name', 'asset_name', 'user_id')

class User(db.Model, SerializerMixin):
    __tablename__ = "user"  

    id = db.Column(db.Integer, primary_key=True)
    
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone_number = db.Column(db.String(20), unique=True, nullable=False)
    password= db.Column(db.String(120), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"), nullable=False)

    requests = db.relationship("Request", back_populates="user")

    role = db.relationship("Role", back_populates="users")  
   
    def __repr__(self):
        return f"<User {self.name}>"
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone_number": self.phone_number,
            "role": self.role.name if self.role else None,
            "request": [request.to_dict()for request in self.request]
        }

class Role(db.Model):
    __tablename__ = "roles"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    permissions = db.Column(db.ARRAY(db.String), default=[])    
    users = db.relationship("User", back_populates="role")

    def __repr__(self):
        return f"<Role {self.name}>"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "permissions": self.permissions
        }        