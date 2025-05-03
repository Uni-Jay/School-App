from flask import Blueprint, request, jsonify, current_app  # ✅ updated
from app.extensions import db
from app.models.user import User
from app.models.school_admin import SchoolAdmin
# from app.models.teacher import Teacher
# from app.models.student import Student
# from app.models.parent import Parent
import json
import base64
import os
from werkzeug.utils import secure_filename
from flask_jwt_extended import (
    create_access_token, jwt_required, get_jwt_identity
)
from datetime import datetime

auth = Blueprint('auth', __name__)

auth_bp = Blueprint('auth_bp', __name__, url_prefix='/auth')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file_extension(filename_or_ext):
    ext = filename_or_ext.rsplit('.', 1)[-1].lower()
    return ext in ALLOWED_EXTENSIONS

@auth_bp.route('/register', methods=['POST'])
def register():
    if request.content_type.startswith('multipart/form-data'):
        data = request.form
        avatar_file = request.files.get('image')
    else:
        data = request.get_json()
        avatar_file = None

    try:
        full_name = data.get('full_name')
        email = data.get('email')
        phone_number = data.get('phone_number')
        dob = data.get('dob')
        religion = data.get('religion')
        gender = data.get('gender')
        address = data.get('address')
        password = data.get('password')
        role = data.get('role', 'super_admin')

        avatar_filename = None
        upload_folder = current_app.config['UPLOAD_FOLDER']
        timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S%f")

        if avatar_file:
            ext = os.path.splitext(avatar_file.filename)[1].lower().lstrip('.')
            if not allowed_file_extension(ext):
                return jsonify({'error': 'Invalid image type. Allowed: png, jpg, jpeg, gif'}), 400

            avatar_filename = secure_filename(f"{email}_{timestamp}.{ext}")
            filepath = os.path.join(upload_folder, avatar_filename)
            avatar_file.save(filepath)

        elif data.get('image'):
            avatar_data = data.get('image')
            try:
                if ',' in avatar_data:
                    header, encoded = avatar_data.split(",", 1)
                    ext = header.split("/")[1].split(";")[0]
                else:
                    encoded = avatar_data
                    ext = "png"  # fallback default

                if not allowed_file_extension(ext):
                    return jsonify({'error': 'Invalid image type. Allowed: png, jpg, jpeg, gif'}), 400

                avatar_filename = secure_filename(f"{email}_{timestamp}.{ext}")
                filepath = os.path.join(upload_folder, avatar_filename)

                with open(filepath, "wb") as f:
                    f.write(base64.b64decode(encoded))
            except Exception as e:
                return jsonify({'error': f'Failed to process image: {str(e)}'}), 400

        user = User(
            full_name=full_name,
            email=email,
            phone_number=phone_number,
            dob=datetime.strptime(dob, '%Y-%m-%d'),
            religion=religion,
            gender=gender,
            address=address,
            role=role,
            school_id=data.get('school_id'),
            image=avatar_filename
        )
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        return jsonify({'message': 'Super admin registered successfully!'}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Email and password are required'}), 400

    email = data['email']
    password = data['password']

    # Try each user type
    user_models = [
        ("super_admin", User),
        ("school_admin", SchoolAdmin),
        # ("teacher", Teacher),
        # ("student", Student),
        # ("parent", Parent),
    ]

    for role_name, model in user_models:
        user = model.query.filter_by(email=email).first()
        if user and user.check_password(password):
            identity = json.dumps({
                "user_id": user.id,
                "role": role_name,
                "school_id": getattr(user, "school_id", None),
            })
            access_token = create_access_token(identity=identity)
            return jsonify({'access_token': access_token}), 200

    return jsonify({'error': 'Invalid credentials'}), 401




@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    # Implement token revocation logic here if needed
    return jsonify({'message': 'Successfully logged out'}), 200
