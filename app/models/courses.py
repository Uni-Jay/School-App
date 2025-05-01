from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(100), nullable=False)
    course_code = db.Column(db.String(50), nullable=False, unique=True)
    school_id = db.Column(db.Integer, db.ForeignKey('school.id'), nullable=False)
    school_super_admin_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    school = db.relationship('School', backref='courses')
    school_super_admin = db.relationship('User', backref='courses')