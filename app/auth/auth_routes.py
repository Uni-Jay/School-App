from flask import Blueprint, request, jsonify
from models import db, User
from flask_jwt_extended import (
    create_access_token, jwt_required, get_jwt_identity
)
from datetime import datetime

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    required_fields = ['full_name', 'email', 'phone_number', 'dob', 'religion',
                       'gender', 'password', 'address']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already registered'}), 400

    user = User(
        full_name=data['full_name'],
        email=data['email'],
        phone_number=data['phone_number'],
        dob=datetime.strptime(data['dob'], '%Y-%m-%d'),
        religion=data['religion'],
        gender=data['gender'],
        address=data['address'],
        role='superadmin',
        school_id=data.get('school_id')  # None for general superadmin
    )
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'Superadmin registered successfully'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Email and password are required'}), 400

    user = User.query.filter_by(email=data['email']).first()
    if not user or not user.check_password(data['password']):
        return jsonify({'error': 'Invalid credentials'}), 401

    access_token = create_access_token(identity=user.id)
    return jsonify({'access_token': access_token}), 200

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    # Implement token revocation logic here if needed
    return jsonify({'message': 'Successfully logged out'}), 200
