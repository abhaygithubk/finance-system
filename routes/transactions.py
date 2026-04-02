from flask import Blueprint, request, jsonify
from services.transaction_service import (
    validate_transaction_data, create_transaction, get_all_transactions,
    get_transaction_by_id, update_transaction, delete_transaction
)
from utils.role_guard import require_role

transactions_bp = Blueprint('transactions', __name__)


@transactions_bp.route('/', methods=['GET'])
def list_transactions():
    """
    GET /api/transactions/
    Optional query params: type, category, user_id, date_from, date_to
    Role: viewer, analyst, admin
    """
    filters = {
        'type': request.args.get('type'),
        'category': request.args.get('category'),
        'user_id': request.args.get('user_id'),
        'date_from': request.args.get('date_from'),
        'date_to': request.args.get('date_to'),
    }
    transactions = get_all_transactions(filters)
    return jsonify({
        'count': len(transactions),
        'transactions': [t.to_dict() for t in transactions]
    }), 200


@transactions_bp.route('/<int:transaction_id>', methods=['GET'])
def get_transaction(transaction_id):
    """GET /api/transactions/<id>"""
    transaction = get_transaction_by_id(transaction_id)
    if not transaction:
        return jsonify({'error': f'Transaction with id {transaction_id} not found'}), 404
    return jsonify(transaction.to_dict()), 200


@transactions_bp.route('/', methods=['POST'])
def add_transaction():
    """
    POST /api/transactions/
    Body: { amount, type, category, date, user_id, notes (optional) }
    Role: analyst, admin
    """
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Request body must be JSON'}), 400

    # Role check via header (simple simulation)
    role = request.headers.get('X-User-Role', 'viewer')
    if role not in ['analyst', 'admin']:
        return jsonify({'error': 'Permission denied. analyst or admin role required'}), 403

    is_valid, error = validate_transaction_data(data)
    if not is_valid:
        return jsonify({'error': error}), 422

    transaction = create_transaction(data)
    return jsonify({
        'message': 'Transaction created successfully',
        'transaction': transaction.to_dict()
    }), 201


@transactions_bp.route('/<int:transaction_id>', methods=['PUT'])
def edit_transaction(transaction_id):
    """
    PUT /api/transactions/<id>
    Role: analyst, admin
    """
    role = request.headers.get('X-User-Role', 'viewer')
    if role not in ['analyst', 'admin']:
        return jsonify({'error': 'Permission denied. analyst or admin role required'}), 403

    transaction = get_transaction_by_id(transaction_id)
    if not transaction:
        return jsonify({'error': f'Transaction with id {transaction_id} not found'}), 404

    data = request.get_json()
    if not data:
        return jsonify({'error': 'Request body must be JSON'}), 400

    updated, error = update_transaction(transaction, data)
    if error:
        return jsonify({'error': error}), 422

    return jsonify({
        'message': 'Transaction updated successfully',
        'transaction': updated.to_dict()
    }), 200


@transactions_bp.route('/<int:transaction_id>', methods=['DELETE'])
def remove_transaction(transaction_id):
    """
    DELETE /api/transactions/<id>
    Role: admin only
    """
    role = request.headers.get('X-User-Role', 'viewer')
    if role != 'admin':
        return jsonify({'error': 'Permission denied. admin role required'}), 403

    transaction = get_transaction_by_id(transaction_id)
    if not transaction:
        return jsonify({'error': f'Transaction with id {transaction_id} not found'}), 404

    delete_transaction(transaction)
    return jsonify({'message': f'Transaction {transaction_id} deleted successfully'}), 200
