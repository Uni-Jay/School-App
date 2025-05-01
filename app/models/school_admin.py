# app/models/school_admin.py
from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash

class SchoolAdmin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone_number = db.Column(db.String(20))
    image = db.Column(db.String(255))  # avatar or uploaded image
    dob = db.Column(db.Date)
    nationality = db.Column(db.String(100))
    state_of_origin = db.Column(db.String(100))
    local_government = db.Column(db.String(100))
    religion = db.Column(db.String(50))
    gender = db.Column(db.String(20))
    level = db.Column(db.String(20))
    step = db.Column(db.String(20))
    address = db.Column(db.String(255)) 
    role = db.Column(db.String(50))  # e.g., head_admin, assistant_admin
    district = db.Column(db.String(100))
    school_id = db.Column(db.Integer, db.ForeignKey('school.id'), nullable=False)
    employment_date = db.Column(db.Date)
    social_media = db.Column(db.String(255))
    website = db.Column(db.String(255))
    password_hash = db.Column(db.String(255))
    posts = db.Column(db.Text)
    school_super_admin_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    notes = db.Column(db.Text)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
