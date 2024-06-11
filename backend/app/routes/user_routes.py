from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.user import User

user_bp = Blueprint('users', __name__)

@user_bp.route('users/me', methods=['GET'])
@jwt_required()
def get_user():
    current_user_id = get_jwt_identity()
    user = User.get_by_id(current_user_id)
    if not user:
        return jsonify({"message": "User not found", "error": "Not Found", "data": None}), 404

    return jsonify({"message": "Successfully fetched user", "data": user.to_dict(), "error": None}), 200

@user_bp.route('users/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user_by_id(user_id):
    current_user_id = get_jwt_identity()
    if current_user_id != user_id:
        return jsonify({"message": "Cannot get another user", "data": None, "error": "Forbidden"}), 403

    user = User.get_by_id(user_id)
    if not user:
        return jsonify({"message": "User not found", "error": "Not Found", "data": None}), 404

    return jsonify({"message": "Successfully fetched user", "data": user.to_dict(), "error": None}), 200

@user_bp.route('users/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    current_user_id = get_jwt_identity()
    if current_user_id != user_id:
        return jsonify({"message": "Cannot delete another user", "data": None, "error": "Forbidden"}), 403

    user, error = User.delete(user_id)
    if error:
        return jsonify({"message": error, "error": "Not Found", "data": None}), 404

    return jsonify({"message": "Successfully deleted user", "data": None, "error": None}), 200

@user_bp.route('users/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    current_user_id = get_jwt_identity()
    if current_user_id != user_id:
        return jsonify({"message": "Cannot update another user", "data": None, "error": "Forbidden"}), 403

    data = request.json
    user, error = User.update(user_id, data)
    if error:
        return jsonify({"message": error, "error": "Not Found", "data": None}), 404

    return jsonify({"message": "Successfully updated user", "data": user.to_dict(), "error": None}), 200
