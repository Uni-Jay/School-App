from app.extensions import db


class StudentSubjectTeacherClassLink(db.Model):
    __tablename__ = 'student_subject_teacher_class_link'

    id = db.Column(db.Integer, primary_key=True)
    class_id = db.Column(db.Integer, db.ForeignKey('class.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'), nullable=False)

    # Optional: You can add a unique constraint to avoid duplicate entries
    __table_args__ = (db.UniqueConstraint('class_id', 'subject_id', 'student_id', 'teacher_id', name='_student_subject_class_teacher_uc'),)

    # Relationships
    student = db.relationship('Student', backref='subject_links')
    subject = db.relationship('Subject', backref='student_links')
    teacher = db.relationship('Teacher', backref='student_subject_links')
    class_ = db.relationship('Class', backref='student_subject_links')
