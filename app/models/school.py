from datetime import datetime
from app.extensions import db

class School(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    school_name = db.Column(db.String(120), nullable=False)
    school_email = db.Column(db.String(120), unique=True, nullable=False)
    school_phone_number = db.Column(db.String(20), nullable=False)
    school_image = db.Column(db.String(255))
    school_address = db.Column(db.Text, nullable=False)
    school_type = db.Column(db.String(20), nullable=False)  # public, private-registered, private-unregistered
    school_registration_date = db.Column(db.Date)
    school_registration_number = db.Column(db.String(100))
    school_csc_number = db.Column(db.String(100))
    school_website = db.Column(db.String(255))
    school_social_media = db.Column(db.String(255))
    school_super_admin_id = db.Column(db.Integer, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
