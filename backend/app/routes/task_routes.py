from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.task import Task

task_bp = Blueprint('task', __name__)

@task_bp.route('/tasks', methods=['POST'])
@jwt_required()
def create_task():
    data = request.json
    task = Task.create(
        title=data['title'],
        description=data.get('description'),
        due_date=data.get('due_date'),
        category_id=data['category_id']
    )
    return jsonify({"message": "Task created", "data": task.to_dict(), "error": None}), 201

@task_bp.route('/tasks', methods=['GET'])
@jwt_required()
def get_tasks():
    category_id = request.args.get('category_id')
    tasks = Task.get_all(category_id)
    return jsonify({"message": "Tasks fetched",
                    "data": tasks,
                    "category_id": category_id,
                    "error": None}), 200

@task_bp.route('/tasks/<int:task_id>', methods=['GET'])
@jwt_required()
def get_task(task_id):
    category_id = request.args.get('category_id')
    task = Task.get_by_id(task_id, category_id)
    if not task:
        return jsonify({"message": "Task not found", "data": None, "error": "Not Found"}), 404
    return jsonify({"message": "Task fetched", "data": task.to_dict(), "error": None}), 200

@task_bp.route('/tasks/<int:task_id>', methods=['PUT'])
@jwt_required()
def update_task(task_id):
    data = request.json
    category_id = data['category_id']
    task, error = Task.update(
        task_id,
        category_id,
        title=data['title'],
        description=data.get('description'),
        due_date=data.get('due_date')
    )
    if error:
        return jsonify({"message": error, "data": None, "error": "Not Found"}), 404
    return jsonify({"message": "Task updated", "data": task.to_dict(), "error": None}), 200

@task_bp.route('/tasks/<int:task_id>', methods=['DELETE'])
@jwt_required()
def delete_task(task_id):
    category_id = request.args.get('category_id')
    task, error = Task.delete(task_id, category_id)
    if error:
        return jsonify({"message": error, "data": None, "error": "Not Found"}), 404
    return jsonify({"message": "Task deleted", "data": None, "error": None}), 204


@task_bp.route('/tasks/<int:task_id>/tags/<int:tag_id>', methods=['POST'])
@jwt_required()
def add_tag_to_task(task_id, tag_id):
    task, error = Task.add_tag(task_id, tag_id)
    if error:
        return jsonify({"message": error, "data": None, "error": "Conflict"}), 409
    return jsonify({"message": "Tag added to task", "data": task.to_dict(), "error": None}), 200

@task_bp.route('/tasks/<int:task_id>/tags/<int:tag_id>', methods=['DELETE'])
@jwt_required()
def remove_tag_from_task(task_id, tag_id):
    task, error = Task.remove_tag(task_id, tag_id)
    if error:
        return jsonify({"message": error, "data": None, "error": "Conflict"}), 409
    return jsonify({"message": "Tag removed from task", "data": task.to_dict(), "error": None}), 200