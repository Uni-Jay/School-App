from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone_number = db.Column(db.String(20), unique=True, nullable=False)
    dob = db.Column(db.Date, nullable=False)
    religion = db.Column(db.String(50))
    image = db.Column(db.String(255))  # optional
    gender = db.Column(db.String(10))
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='superadmin')
    address = db.Column(db.String(255))
    school_id = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    # is_active = db.Column(db.Boolean, default=True)


    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
