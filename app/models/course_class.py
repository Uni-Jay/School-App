
from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.courses import Subject


class SubjectClassLink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey('school_class.id'), nullable=False)
