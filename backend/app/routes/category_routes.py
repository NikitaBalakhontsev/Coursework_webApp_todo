from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.category import Category

category_bp = Blueprint('category', __name__)

@category_bp.route('/categories', methods=['POST'])
@jwt_required()
def create_category():
    data = request.json
    current_user_id = get_jwt_identity()
    category = Category.create(name=data['name'], user_id=current_user_id)
    return jsonify({"message": "Category created", "data": category.to_dict(), "error": None}), 201

@category_bp.route('/categories', methods=['GET'])
@jwt_required()
def get_categories():
    current_user_id = get_jwt_identity()
    categories = Category.get_all(user_id=current_user_id)
    return jsonify({"message": "Categories fetched", "data": categories, "error": None}), 200

@category_bp.route('/categories/<int:category_id>', methods=['GET'])
@jwt_required()
def get_category(category_id):
    current_user_id = get_jwt_identity()
    category = Category.get_by_id(category_id, current_user_id)
    if not category:
        return jsonify({"message": "Category not found", "data": None, "error": "Not Found"}), 404
    return jsonify({"message": "Category fetched", "data": category.to_dict(), "error": None}), 200

@category_bp.route('/categories/<int:category_id>', methods=['PUT'])
@jwt_required()
def update_category(category_id):
    data = request.json
    current_user_id = get_jwt_identity()
    category, error = Category.update(category_id, current_user_id, name=data['name'])
    if error:
        return jsonify({"message": error, "data": None, "error": "Not Found"}), 404
    return jsonify({"message": "Category updated", "data": category.to_dict(), "error": None}), 200

@category_bp.route('/categories/<int:category_id>', methods=['DELETE'])
@jwt_required()
def delete_category(category_id):
    current_user_id = get_jwt_identity()
    category, error = Category.delete(category_id, current_user_id)
    if error:
        return jsonify({"message": error, "data": None, "error": "Not Found"}), 404
    return jsonify({"message": "Category deleted", "data": None, "error": None}), 204