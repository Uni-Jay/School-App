from flask import Blueprint, request, jsonify
from models import Course  # Adjust the import based on your actual file structure
from app.extensions import db

course_bp = Blueprint('course_bp', __name__,url_prefix='/course')

# 1. Add Course
@course_bp.route('/add', methods=['POST'])
def add_course():
    data = request.get_json()

    required_fields = ['course_name', 'course_code', 'school_id', 'school_super_admin_id']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"{field} is required"}), 400

    course = Course(
        course_name=data['course_name'],
        course_code=data['course_code'],
        school_id=data['school_id'],
        school_super_admin_id=data['school_super_admin_id']
    )
    db.session.add(course)
    db.session.commit()

    return jsonify({
        "message": "Course added successfully",
        "course_id": course.id
    }), 201


# 2. Edit Course by ID
@course_bp.route('/edit/<int:course_id>', methods=['PUT'])
def edit_course(course_id):
    data = request.get_json()
    course = Course.query.get(course_id)

    if not course:
        return jsonify({"error": "Course not found"}), 404

    course.course_name = data.get('course_name', course.course_name)
    course.course_code = data.get('course_code', course.course_code)

    db.session.commit()

    return jsonify({"message": "Course updated successfully"}), 200


# 3. Get All Courses
@course_bp.route('/all', methods=['GET'])
def get_all_courses():
    courses = Course.query.all()
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


# 4. Get All Courses by School ID
@course_bp.route('/school/<int:school_id>', methods=['GET'])
def get_courses_by_school(school_id):
    courses = Course.query.filter_by(school_id=school_id).all()
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


# 5. Get Course by Course ID
@course_bp.route('/<int:course_id>', methods=['GET'])
def get_course_by_id(course_id):
    course = Course.query.get(course_id)

    if not course:
        return jsonify({"error": "Course not found"}), 404

    result = {
        "id": course.id,
        "course_name": course.course_name,
        "course_code": course.course_code,
        "school_id": course.school_id,
        "school_super_admin_id": course.school_super_admin_id
    }
    return jsonify(result), 200
