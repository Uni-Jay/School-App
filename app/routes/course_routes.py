from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Course, User
from app.extensions import db

course_bp = Blueprint('course_bp', __name__)

# Add Course
@course_bp.route('/add', methods=['POST'])
@jwt_required()
def add_course():
    data = request.json
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    if not user or user.role not in ['super_admin', 'school_super_admin']:
        return jsonify({"error": "Unauthorized"}), 403

    course = Course(
        course_name=data.get('course_name'),
        course_code=data.get('course_code'),
        school_id=data.get('school_id'),
        school_super_admin_id=current_user_id
    )
    db.session.add(course)
    db.session.commit()

    return jsonify({"message": "Course added successfully"}), 201

# Get All Courses (only active)
@course_bp.route('/all', methods=['GET'])
@jwt_required()
def get_all_courses():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    if not user or not user.is_active:
        return jsonify({"error": "Unauthorized or inactive"}), 403

    courses = Course.query.filter_by(is_active=True).all()
    result = [
        {
            "id": course.id,
            "course_name": course.course_name,
            "course_code": course.course_code,
            "school_id": course.school_id,
            "school_super_admin_id": course.school_super_admin_id
        } for course in courses
    ]
    return jsonify(result), 200

# Get Course by ID
@course_bp.route('/<int:course_id>', methods=['GET'])
@jwt_required()
def get_course_by_id(course_id):
    course = Course.query.get(course_id)
    if not course or not course.is_active:
        return jsonify({"error": "Course not found or inactive"}), 404

    result = {
        "id": course.id,
        "course_name": course.course_name,
        "course_code": course.course_code,
        "school_id": course.school_id,
        "school_super_admin_id": course.school_super_admin_id
    }
    return jsonify(result), 200

# Edit Course
@course_bp.route('/edit/<int:course_id>', methods=['PUT'])
@jwt_required()
def edit_course(course_id):
    data = request.json
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    course = Course.query.get(course_id)
    if not course:
        return jsonify({"error": "Course not found"}), 404

    if user.role not in ['super_admin', 'school_super_admin'] or user.id != course.school_super_admin_id:
        return jsonify({"error": "Unauthorized"}), 403

    course.course_name = data.get('course_name', course.course_name)
    course.course_code = data.get('course_code', course.course_code)
    db.session.commit()

    return jsonify({"message": "Course updated successfully"}), 200

# Soft Delete Course
@course_bp.route('/deactivate/<int:course_id>', methods=['PUT'])
@jwt_required()
def deactivate_course(course_id):
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    if not user or user.role not in ['super_admin', 'school_super_admin']:
        return jsonify({"error": "Unauthorized"}), 403

    course = Course.query.get(course_id)
    if not course:
        return jsonify({"error": "Course not found"}), 404

    course.is_active = False
    db.session.commit()

    return jsonify({"message": "Course deactivated successfully"}), 200