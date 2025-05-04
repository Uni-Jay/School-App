from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import User
from datetime import datetime
from flask_jwt_extended import jwt_required, get_jwt_identity

user_bp = Blueprint('user', __name__)

# Get all active users
@user_bp.route('/users', methods=['GET'])
@jwt_required()
def get_all_users():
    users = User.query.filter_by(is_active=True).all()
    return jsonify([
        {
            "id": u.id,
            "full_name": u.full_name,
            "email": u.email,
            "phone_number": u.phone_number,
            "dob": u.dob.strftime('%Y-%m-%d') if u.dob else None,
            "religion": u.religion,
            "image": u.image,
            "gender": u.gender,
            "role": u.role,
            "address": u.address,
            "school_id": u.school_id
        } for u in users
    ]), 200

# Get a single user by ID
@user_bp.route('/users/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    if not user.is_active:
        return jsonify({"error": "User has been deactivated"}), 404

    return jsonify({
        "id": user.id,
        "full_name": user.full_name,
        "email": user.email,
        "phone_number": user.phone_number,
        "dob": user.dob.strftime('%Y-%m-%d') if user.dob else None,
        "religion": user.religion,
        "image": user.image,
        "gender": user.gender,
        "role": user.role,
        "address": user.address,
        "school_id": user.school_id
    }), 200

# Add user
@user_bp.route('/users', methods=['POST'])
@jwt_required()
def add_user():
    if request.content_type.startswith('multipart/form-data'):
        data = request.form
        image_file = request.files.get('image')
        image_filename = image_file.filename if image_file else None
    else:
        data = request.get_json()
        image_filename = data.get('image')

    user = User(
        full_name=data['full_name'],
        email=data['email'],
        phone_number=data['phone_number'],
        dob=datetime.strptime(data['dob'], '%Y-%m-%d'),
        religion=data.get('religion'),
        image=image_filename,
        gender=data.get('gender'),
        role=data.get('role', 'superadmin'),
        address=data.get('address'),
        school_id=data.get('school_id'),
        is_active=True
    )
    user.set_password(data['password'])

    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User created successfully"}), 201

# Edit user
@user_bp.route('/users/<int:user_id>', methods=['PUT'])
@jwt_required()
def edit_user(user_id):
    user = User.query.get_or_404(user_id)

    if request.content_type.startswith('multipart/form-data'):
        data = request.form
        image_file = request.files.get('image')
        if image_file:
            user.image = image_file.filename
    else:
        data = request.get_json()
        user.image = data.get('image', user.image)

    user.full_name = data.get('full_name', user.full_name)
    user.phone_number = data.get('phone_number', user.phone_number)
    user.religion = data.get('religion', user.religion)
    user.gender = data.get('gender', user.gender)
    user.role = data.get('role', user.role)
    user.address = data.get('address', user.address)
    user.school_id = data.get('school_id', user.school_id)

    db.session.commit()
    return jsonify({"message": "User updated successfully"}), 200

# Soft delete user
# @user_bp.route('/users/<int:user_id>', methods=['DELETE'])
# @jwt_required()
# def delete_user(user_id):
#     user = User.query.get_or_404(user_id)
#     user.is_active = False
#     db.session.commit()
#     return jsonify({"message": "User deactivated successfully"}), 200

# Reactivate user
# @user_bp.route('/users/<int:user_id>/reactivate', methods=['PATCH'])
# @jwt_required()
# def reactivate_user(user_id):
#     user = User.query.get_or_404(user_id)
#     user.is_active = True
#     db.session.commit()
#     return jsonify({"message": "User reactivated successfully"}), 200
