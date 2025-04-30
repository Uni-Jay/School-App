from functools import wraps
from flask import request, jsonify, g
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from app.models import User
import json

def get_current_user():
    try:
        verify_jwt_in_request()
        identity = get_jwt_identity()
        return identity['user_id'], identity['role'], identity.get('school_id')
    except Exception:
        return None, None, None

def role_required(*allowed_roles):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            user_id, role, _ = get_current_user()

            if role == 'super_admin':
                return f(*args, **kwargs)
            
            if not role or role not in allowed_roles:
                return jsonify({'error': 'Access denied'}), 403
            g.user_id = user_id
            g.user_role = role
            return f(*args, **kwargs)
        return wrapper
    return decorator

def same_school_required():
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            user_id, role, user_school_id = get_current_user()

            # Try to get school_id from path, query, or JSON
            school_id = (
                kwargs.get('school_id') or
                request.args.get('school_id') or
                request.get_json(silent=True, force=True).get('school_id') if request.is_json else None
            )

            if role == 'super_admin':
                return f(*args, **kwargs)

            if user_school_id is None or school_id is None or int(user_school_id) != int(school_id):
                return jsonify({'error': 'Access denied: School mismatch'}), 403

            g.user_id = user_id
            g.user_role = role
            return f(*args, **kwargs)
        return wrapper
    return decorator
