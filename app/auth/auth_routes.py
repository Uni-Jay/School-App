from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.user import User
import json
from flask_jwt_extended import (
    create_access_token, jwt_required, get_jwt_identity
)
from datetime import datetime

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['POST'])
def register():
    # print("Register endpoint hit")
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
        role='super_admin',
        school_id=data.get('school_id')
    )
    user.set_password(data['password'])  # Correct password hashing

    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'Superadmin registered successfully'}), 201

import json

@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Email and password are required'}), 400

    user = User.query.filter_by(email=data['email']).first()
    if not user or not user.check_password(data['password']):
        return jsonify({'error': 'Invalid credentials'}), 401

    identity = json.dumps({
        "user_id": user.id,
        "role": user.role,
        "school_id": user.school_id if user.role != 'super_admin' else None,
    })
    access_token = create_access_token(identity=identity)
    return jsonify({'access_token': access_token}), 200



@auth.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    # Implement token revocation logic here if needed
    return jsonify({'message': 'Successfully logged out'}), 200
