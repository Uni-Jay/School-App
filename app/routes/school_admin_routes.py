# app/routes/school_admin_routes.py
from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.school_admin import SchoolAdmin
from app.models.school import School
from app.utils.email import send_email  # You'll create this
from datetime import datetime
import random

school_admin_bp = Blueprint('school_admin', __name__, url_prefix='/school-admin')

@school_admin_bp.route('/add', methods=['POST'])
def add_school_admin():
    data = request.get_json()

    required_fields = ['full_name', 'email', 'school_id', 'school_super_admin_id', 'dob']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"{field} is required"}), 400

    if SchoolAdmin.query.filter_by(email=data['email']).first():
        return jsonify({"error": "Email already exists"}), 400

    birth_year = datetime.strptime(data['dob'], "%Y-%m-%d").year
    special_chars = ['@', '#', '$', '%', '&', '*']
    password = f"{data['full_name'].replace(' ', '')}{birth_year}{random.choice(special_chars)}"

    admin = SchoolAdmin(
        full_name=data['full_name'],
        email=data['email'],
        phone_number=data.get('phone_number'),
        image=data.get('image'),
        dob=datetime.strptime(data['dob'], "%Y-%m-%d"),
        nationality=data.get('nationality'),
        state_of_origin=data.get('state_of_origin'),
        local_government=data.get('local_government'),
        religion=data.get('religion'),
        gender=data.get('gender'),
        level=data.get('level'),
        step=data.get('step'),
        role=data.get('role'),
        district=data.get('district'),
        school_id=data['school_id'],
        employment_date=datetime.strptime(data['employment_date'], "%Y-%m-%d") if data.get('employment_date') else None,
        social_media=data.get('social_media'),
        website=data.get('website'),
        posts=data.get('posts'),
        school_super_admin_id=data['school_super_admin_id'],
        notes=data.get('notes')
    )
    admin.set_password(password)

    db.session.add(admin)
    db.session.commit()

    # Get school name
    school = School.query.get(admin.school_id)
    school_name = school.school_name if school else "your school"

    # Send welcome email
    send_email(
        to=admin.email,
        subject="Welcome to Our School",
        body=f"""
        Hello {admin.full_name},

        Welcome to {school_name}!

        We are excited to have you on board as a school admin. Your role is crucial in ensuring the smooth operation of our school.

        Your login credentials:
        Username: {admin.email}
        Password: {password}

        Regards,
        School Management System
        """
    )

    return jsonify({"message": "School admin added successfully", "admin_id": admin.id}), 201
