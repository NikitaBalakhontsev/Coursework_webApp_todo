import datetime

from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.models.user import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/authorize', methods=['POST'])
def authorize():
    data = request.json
    if not data:
        return jsonify({"message": "No input data provided", "data": None, "error": "Bad request"}), 400

    user, error = User.create(data['username'], data['email'], data['password'])
    if error:
        return jsonify({"message": error, "data": None, "error": "Conflict"}), 409

    return jsonify({"message": "Successfully registered", "data": {"user": user.to_dict()}, "error": None}), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    if not data:
        return jsonify({"message": "Please provide user details", "data": None, "error": "Bad request"}), 400

    user = User.query.filter_by(email=data['email']).first()
    if not user:
        return jsonify({"message": "User not found", "data": None, "error": "Unauthorized"}), 401

    if not user.check_password(data['password']):
        return jsonify({"message": "Invalid password", "data": None, "error": "Unauthorized"}), 401

    access_token = create_access_token(identity=user.id, expires_delta=datetime.timedelta(hours=12))
    return jsonify({"message": "Successfully fetched auth token", "data": {"token": access_token}, "error": None}), 200


@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    # Implement token revoking if necessary
    return jsonify({"message": "Successfully logged out", "data": None, "error": None}), 200


@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=False)
def refresh():
    current_user_id = get_jwt_identity()
    new_token = create_access_token(identity=current_user_id, expires_delta=datetime.timedelta(hours=12))
    return jsonify({"message": "Successfully refreshed token", "data": {"token": new_token}, "error": None}), 200


@auth_bp.route('/validate_token', methods=['POST'])
@jwt_required()
def validate_token():
    current_user_id = get_jwt_identity()
    return jsonify({"message": "Successfully validate token", "data": {"user_id": current_user_id}, "error": None}), 200