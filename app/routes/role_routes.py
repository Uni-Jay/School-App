# routes/role_routes.py
from flask import Blueprint, request, jsonify
from models.role import Role
from flask_jwt_extended import jwt_required
from app.extensions import db

role_bp = Blueprint("roles", __name__, url_prefix="/roles")

@role_bp.route("", methods=["POST"])
@jwt_required()
def add_role():
    data = request.json
    new_role = Role(name=data["name"], description=data.get("description"))
    db.session.add(new_role)
    db.session.commit()
    return jsonify({"message": "Role created"}), 201

@role_bp.route("", methods=["GET"])
@jwt_required()
def get_all_roles():
    roles = Role.query.all()
    return jsonify([{"id": r.id, "name": r.name, "description": r.description} for r in roles])

@role_bp.route("/<int:role_id>", methods=["GET"])
@jwt_required()
def get_role(role_id):
    role = Role.query.get_or_404(role_id)
    return jsonify({"id": role.id, "name": role.name, "description": role.description})

@role_bp.route("/<int:role_id>", methods=["PUT"])
@jwt_required()
def update_role(role_id):
    role = Role.query.get_or_404(role_id)
    data = request.json
    role.name = data.get("name", role.name)
    role.description = data.get("description", role.description)
    db.session.commit()
    return jsonify({"message": "Role updated"})

@role_bp.route("/<int:role_id>", methods=["DELETE"])
@jwt_required()
def delete_role(role_id):
    role = Role.query.get_or_404(role_id)
    db.session.delete(role)
    db.session.commit()
    return jsonify({"message": "Role deleted"})
