from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.tag import Tag, db

tag_bp = Blueprint('tag', __name__)

@tag_bp.route('/tags', methods=['POST'])
@jwt_required()
def create_tag():
    current_user_id = get_jwt_identity()
    data = request.json
    description = data.get('description')
    color = data.get('color')

    if not description and not color:
        return jsonify({"message": "Either description or color must be provided", "data": None, "error": "Bad Request"}), 400

    existing_tag = Tag.query.filter_by(description=description, color=color, user_id=current_user_id).first()
    if existing_tag:
        return jsonify({
            "message": "Tag with same description and color already exists",
            "data": {"existing_tag_id": existing_tag.id},
            "error": "Conflict"
        }), 409

    new_tag = Tag(description=description, color=color, user_id=current_user_id)
    db.session.add(new_tag)
    db.session.commit()

    return jsonify({"message": "Tag created", "data": new_tag.to_dict(), "error": None}), 201

@tag_bp.route('/tags', methods=['GET'])
@jwt_required()
def get_tags():
    current_user_id = get_jwt_identity()
    tags = Tag.query.filter_by(user_id=current_user_id).all()
    tags_data = [tag.to_dict() for tag in tags]
    return jsonify({"message": "Tags fetched", "data": tags_data, "error": None}), 200

@tag_bp.route('/tags/<int:tag_id>', methods=['GET'])
@jwt_required()
def get_tag(tag_id):
    current_user_id = get_jwt_identity()
    tag = Tag.query.filter_by(id=tag_id, user_id=current_user_id).first()
    if not tag:
        return jsonify({"message": "Tag not found", "data": None, "error": "Not Found"}), 404
    return jsonify({"message": "Tag fetched", "data": tag.to_dict(), "error": None}), 200

@tag_bp.route('/tags/<int:tag_id>', methods=['PUT'])
@jwt_required()
def update_tag(tag_id):
    current_user_id = get_jwt_identity()
    data = request.json
    description = data.get('description')
    color = data.get('color')

    if not description and not color:
        return jsonify({"message": "Either description or color must be provided", "data": None, "error": "Bad Request"}), 400

    tag = Tag.query.filter_by(id=tag_id, user_id=current_user_id).first()
    if not tag:
        return jsonify({"message": "Tag not found", "data": None, "error": "Not Found"}), 404

    existing_tag = Tag.query.filter_by(description=description, color=color, user_id=current_user_id).first()
    if existing_tag and existing_tag.id != tag.id:
        return jsonify({
            "message": "Tag with same description and color already exists",
            "data": {"existing_tag_id": existing_tag.id},
            "error": "Conflict"
        }), 409

    tag.description = description
    tag.color = color
    db.session.commit()

    return jsonify({"message": "Tag updated", "data": tag.to_dict(), "error": None}), 200

@tag_bp.route('/tags/<int:tag_id>', methods=['DELETE'])
@jwt_required()
def delete_tag(tag_id):
    current_user_id = get_jwt_identity()
    tag = Tag.query.filter_by(id=tag_id, user_id=current_user_id).first()
    if not tag:
        return jsonify({"message": "Tag not found", "data": None, "error": "Not Found"}), 404

    db.session.delete(tag)
    db.session.commit()

    return jsonify({"message": "Tag deleted", "data": None, "error": None}), 204
