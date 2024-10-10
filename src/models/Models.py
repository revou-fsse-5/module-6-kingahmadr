from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy
# from flask_sqlalchemy.sql import func    
from werkzeug.security import generate_password_hash, check_password_hash
 
db = SQLAlchemy()
 
class AnimalModel(db.Model):
    __tablename__ = 'animals'
 
    id = db.Column(db.BigInteger, primary_key = True)
    name = db.Column(db.String(), nullable=True)
    species = db.Column(db.String(), nullable=True)
    age = db.Column(db.Integer(), nullable=True)
    special_requirement = db.Column(db.String(), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    
 
    def __init__(self, name=None, species=None ,age=None ,special_requirement=None):
        self.name = name
        self.species = species
        self.age = age
        self.special_requirement = special_requirement
 
    def __repr__(self):
        return f"{self.name}:{self.species}:{self.age}:{self.special_requirement}"
    
class EmployeeModel(db.Model):
    __tablename__ = 'employees'
 
    id = db.Column(db.BigInteger, primary_key = True)
    name = db.Column(db.String(), nullable=True)
    email = db.Column(db.String(), nullable=True)
    phone = db.Column(db.String(), nullable=True)
    role = db.Column(db.String(), nullable=True)
    schedule = db.Column(db.String(), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    
    def __init__(self, name=None, email=None, phone=None, role=None, schedule=None):
        self.name = name
        self.email = email
        self.phone = phone
        self.role = role
        self.schedule = schedule

 
    def __repr__(self):
        return f"{self.name}:{self.email}:{self.phone}:{self.role}:{self.schedule}"
    
class TestModel(db.Model):
    __tablename__ = 'test_table'
 
    id = db.Column(db.BigInteger, primary_key = True)
    name = db.Column(db.String(), nullable=True)
    email = db.Column(db.String(), nullable=True)
    phone = db.Column(db.String(), nullable=True)
    role = db.Column(db.String(), nullable=True)
    schedule = db.Column(db.String(), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    
    def __init__(self, name=None, email=None, phone=None, role=None, schedule=None):
        self.name = name
        self.email = email
        self.phone = phone
        self.role = role
        self.schedule = schedule

 
    def __repr__(self):
        return f"{self.name}:{self.email}:{self.phone}:{self.role}:{self.schedule}"

class User(db.Model):
    __tablename__ = "users"
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f'<User {self.email}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)