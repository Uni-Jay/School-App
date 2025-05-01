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
    <html>
    <body style="font-family: Arial, sans-serif; color: #333; padding: 20px;">
        <h2 style="color: #2e6c80;">Hello {admin.full_name},</h2>
        <p>Welcome to <strong>{school_name}</strong>!</p>

        <p>We are excited to have you on board as a school admin. Your role is crucial in ensuring the smooth operation of our school.</p>

        <h3 style="margin-top: 30px;">Your Login Credentials</h3>
        <table style="border-collapse: collapse; width: 100%;">
            <tr>
                <td style="padding: 8px; font-weight: bold;">Username:</td>
                <td style="padding: 8px;">{admin.email}</td>
            </tr>
            <tr>
                <td style="padding: 8px; font-weight: bold;">Password:</td>
                <td style="padding: 8px;">{password}</td>
            </tr>
        </table>

        <p style="margin-top: 30px;">Regards,<br><strong>{school_name}</strong></p>
    </body>
    </html>
    """,
    is_html=True
)


    return jsonify({"message": "School admin added successfully", "admin_id": admin.id}), 201

@school_admin_bp.route('/edit/<int:admin_id>', methods=['PUT'])
def edit_school_admin(admin_id):
    data = request.get_json()
    admin = SchoolAdmin.query.get(admin_id)

    if not admin:
        return jsonify({"error": "School admin not found"}), 404

    # Update allowed fields only (email & password are excluded)
    admin.full_name = data.get('full_name', admin.full_name)
    admin.phone_number = data.get('phone_number', admin.phone_number)
    admin.image = data.get('image', admin.image)
    admin.dob = datetime.strptime(data['dob'], "%Y-%m-%d") if data.get('dob') else admin.dob
    admin.nationality = data.get('nationality', admin.nationality)
    admin.state_of_origin = data.get('state_of_origin', admin.state_of_origin)
    admin.local_government = data.get('local_government', admin.local_government)
    admin.religion = data.get('religion', admin.religion)
    admin.gender = data.get('gender', admin.gender)
    admin.level = data.get('level', admin.level)
    admin.step = data.get('step', admin.step)
    admin.role = data.get('role', admin.role)
    admin.district = data.get('district', admin.district)
    admin.school_id = data.get('school_id', admin.school_id)
    admin.employment_date = datetime.strptime(data['employment_date'], "%Y-%m-%d") if data.get('employment_date') else admin.employment_date
    admin.social_media = data.get('social_media', admin.social_media)
    admin.website = data.get('website', admin.website)
    admin.posts = data.get('posts', admin.posts)
    admin.school_super_admin_id = data.get('school_super_admin_id', admin.school_super_admin_id)
    admin.notes = data.get('notes', admin.notes)

    db.session.commit()

    # Fetch updated school
    school = School.query.get(admin.school_id)
    school_name = school.school_name if school else "your school"

    # Send update email
    send_email(
        to=admin.email,
        subject="Your Profile Has Been Updated",
        body=f"""
        <html>
        <body style="font-family: Arial, sans-serif; color: #333; padding: 20px;">
            <h2 style="color: #2e6c80;">Hello {admin.full_name},</h2>

            <p>Your profile information has been successfully updated in the {school_name}.</p>

            <h3 style="margin-top: 20px;">Updated Details:</h3>
            <table style="border-collapse: collapse; width: 100%;">
                <tr><td style="padding: 8px; font-weight: bold;">Full Name:</td><td style="padding: 8px;">{admin.full_name}</td></tr>
                <tr><td style="padding: 8px; font-weight: bold;">Phone Number:</td><td style="padding: 8px;">{admin.phone_number or "N/A"}</td></tr>
                <tr><td style="padding: 8px; font-weight: bold;">Date of Birth:</td><td style="padding: 8px;">{admin.dob or "N/A"}</td></tr>
                <tr><td style="padding: 8px; font-weight: bold;">Role:</td><td style="padding: 8px;">{admin.role or "N/A"}</td></tr>
                <tr><td style="padding: 8px; font-weight: bold;">School:</td><td style="padding: 8px;">{school.school_name if school else "N/A"}</td></tr>
                <tr><td style="padding: 8px; font-weight: bold;">Address:</td><td style="padding: 8px;">{admin.address or "N/A"}</td></tr>
                <tr><td style="padding: 8px; font-weight: bold;">Religion:</td><td style="padding: 8px;">{admin.religion or "N/A"}</td></tr>
                <tr><td style="padding: 8px; font-weight: bold;">Nationailty:</td><td style="padding: 8px;">{admin.nationality or "N/A"}</td></tr>
                <tr><td style="padding: 8px; font-weight: bold;">State of Origin:</td><td style="padding: 8px;">{admin.state_of_origin or "N/A"}</td></tr>
                <tr><td style="padding: 8px; font-weight: bold;">Local Govt:</td><td style="padding: 8px;">{admin.local_government or "N/A"}</td></tr>
                <tr><td style="padding: 8px; font-weight: bold;">Gender:</td><td style="padding: 8px;">{admin.gender or "N/A"}</td></tr>
                <tr><td style="padding: 8px; font-weight: bold;">Level:</td><td style="padding: 8px;">{admin.level or "N/A"}</td></tr>
                <tr><td style="padding: 8px; font-weight: bold;">Step:</td><td style="padding: 8px;">{admin.step or "N/A"}</td></tr>
                <tr><td style="padding: 8px; font-weight: bold;">Employment Date:</td><td style="padding: 8px;">{admin.employment_date or "N/A"}</td></tr>
                <tr><td style="padding: 8px; font-weight: bold;">Role:</td><td style="padding: 8px;">{admin.role or "N/A"}</td></tr>
            </table>

            <p style="margin-top: 30px;">If you did not request these changes, please contact your school administrator.</p>

            <p>Best regards,<br><strong>{school_name}</strong></p>
        </body>
        </html>
        """,
        is_html=True
    )

    return jsonify({"message": "School admin updated successfully."}), 200
