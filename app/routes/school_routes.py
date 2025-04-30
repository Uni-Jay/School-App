from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.extensions import db
from app.models.school import School
from app.auth.decorators import role_required, same_school_required

school_bp = Blueprint('school', __name__, url_prefix='/school')

# 🔐 Only super_admin can add school
@school_bp.route('/add', methods=['POST'])
@jwt_required()
# @role_required('super_admin')
def add_school():
    data = request.get_json()
    required_fields = ['school_name', 'school_email', 'school_phone_number', 'school_address', 'school_type', 'school_super_admin_id']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"{field} is required"}), 400

    school = School(
        school_name=data['school_name'],
        school_email=data['school_email'],
        school_phone_number=data['school_phone_number'],
        school_image=data.get('school_image'),
        school_address=data['school_address'],
        school_type=data['school_type'],
        school_registration_date=data.get('school_registration_date'),
        school_registration_number=data.get('school_registration_number'),
        school_csc_number=data.get('school_csc_number'),
        school_website=data.get('school_website'),
        school_social_media=data.get('school_social_media'),
        school_super_admin_id=data['school_super_admin_id']
    )
    db.session.add(school)
    db.session.commit()

    return jsonify({"message": "School added successfully", "school_id": school.id}), 201

# 🔐 Only super_admin, school_super_admin, or school_admin of SAME school can edit
@school_bp.route('/edit/<int:school_id>', methods=['PUT'])
@jwt_required()
@role_required('super_admin', 'school_super_admin', 'school_admin')
@same_school_required()
def edit_school(school_id):
    school = School.query.get_or_404(school_id)
    data = request.get_json()

    # Restrict email editing for private-registered
    if school.school_type == 'private-registered' and 'school_email' in data:
        return jsonify({"error": "You cannot edit school_email for registered private schools"}), 403

    # Update allowed fields
    for field in ['school_name', 'school_phone_number', 'school_image', 'school_address',
                  'school_registration_date', 'school_registration_number', 'school_csc_number',
                  'school_website', 'school_social_media', 'school_super_admin_id']:
        if field in data:
            setattr(school, field, data[field])

    db.session.commit()
    return jsonify({"message": "School updated successfully"}), 200

# 🔓 All roles can get school by ID, if same school
@school_bp.route('/<int:school_id>', methods=['GET'])
@jwt_required()
# @role_required('super_admin', 'school_super_admin', 'school_admin', 'teacher', 'parent', 'student')
@same_school_required()
def get_school(school_id):
    school = School.query.get_or_404(school_id)
    return jsonify({col.name: getattr(school, col.name) for col in school.__table__.columns})

# 🔓 All roles can get all schools (optionally restrict later)
@school_bp.route('/', methods=['GET'])
@jwt_required()
@role_required('super_admin', 'school_super_admin', 'school_admin', 'teacher', 'parent', 'student')
def get_all_schools():
    schools = School.query.filter_by(is_active=True).all()
    return jsonify([
        {col.name: getattr(school, col.name) for col in school.__table__.columns}
        for school in schools
    ])

# 🔐 Optional: restrict deactivation to admins
@school_bp.route('/deactivate/<int:school_id>', methods=['DELETE'])
@jwt_required()
# @role_required('super_admin')
def deactivate_school(school_id):
    school = School.query.get_or_404(school_id)
    school.is_active = False
    db.session.commit()
    return jsonify({"message": "School deactivated successfully"}), 200

@school_bp.route('/reactivate/<int:school_id>', methods=['PUT'])
@jwt_required()
# @role_required('super_admin')
def reactivate_school(school_id):
    school = School.query.get_or_404(school_id)
    
    if school.is_active:
        return jsonify({"message": "School is already active"}), 400

    school.is_active = True
    db.session.commit()
    return jsonify({"message": "School reactivated successfully"}), 200
