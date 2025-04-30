from app import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone_number = db.Column(db.String(20), unique=True, nullable=False)
    dob = db.Column(db.Date, nullable=False)
    religion = db.Column(db.String(50))
    image = db.Column(db.String(255))  # URL or file path
    gender = db.Column(db.String(10))
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='superadmin')
    address = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
