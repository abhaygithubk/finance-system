from flask import Blueprint, request, jsonify
from services.user_service import (
    validate_user_data, create_user, get_all_users,
    get_user_by_id, update_user, delete_user
)

users_bp = Blueprint('users', __name__)


@users_bp.route('/', methods=['GET'])
def list_users():
    """GET /api/users/ - Role: admin"""
    role = request.headers.get('X-User-Role', 'viewer')
    if role != 'admin':
        return jsonify({'error': 'Permission denied. admin role required'}), 403

    users = get_all_users()
    return jsonify({
        'count': len(users),
        'users': [u.to_dict() for u in users]
    }), 200


@users_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """GET /api/users/<id> - Role: admin or self"""
    user = get_user_by_id(user_id)
    if not user:
        return jsonify({'error': f'User with id {user_id} not found'}), 404
    return jsonify(user.to_dict()), 200


@users_bp.route('/', methods=['POST'])
def add_user():
    """
    POST /api/users/
    Body: { name, email, role (optional, default: viewer) }
    Role: admin
    """
    role = request.headers.get('X-User-Role', 'viewer')
    if role != 'admin':
        return jsonify({'error': 'Permission denied. admin role required'}), 403

    data = request.get_json()
    if not data:
        return jsonify({'error': 'Request body must be JSON'}), 400

    is_valid, error = validate_user_data(data)
    if not is_valid:
        return jsonify({'error': error}), 422

    user = create_user(data)
    return jsonify({
        'message': 'User created successfully',
        'user': user.to_dict()
    }), 201


@users_bp.route('/<int:user_id>', methods=['PUT'])
def edit_user(user_id):
    """PUT /api/users/<id> - Role: admin"""
    requesting_role = request.headers.get('X-User-Role', 'viewer')

    user = get_user_by_id(user_id)
    if not user:
        return jsonify({'error': f'User with id {user_id} not found'}), 404

    data = request.get_json()
    if not data:
        return jsonify({'error': 'Request body must be JSON'}), 400

    updated, error = update_user(user, data, requesting_role)
    if error:
        return jsonify({'error': error}), 403

    return jsonify({
        'message': 'User updated successfully',
        'user': updated.to_dict()
    }), 200


@users_bp.route('/<int:user_id>', methods=['DELETE'])
def remove_user(user_id):
    """DELETE /api/users/<id> - Role: admin only"""
    requesting_role = request.headers.get('X-User-Role', 'viewer')

    user = get_user_by_id(user_id)
    if not user:
        return jsonify({'error': f'User with id {user_id} not found'}), 404

    success, error = delete_user(user, requesting_role)
    if not success:
        return jsonify({'error': error}), 403

    return jsonify({'message': f'User {user_id} deleted successfully'}), 200
