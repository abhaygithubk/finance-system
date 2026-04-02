from flask import Blueprint, request, jsonify
from services.summary_service import (
    get_summary, get_category_breakdown,
    get_monthly_totals, get_recent_activity
)

summary_bp = Blueprint('summary', __name__)


@summary_bp.route('/', methods=['GET'])
def overview():
    """
    GET /api/summary/
    Optional: ?user_id=<id>
    Returns: total_income, total_expenses, balance, transaction count
    """
    user_id = request.args.get('user_id', type=int)
    data = get_summary(user_id)
    return jsonify(data), 200


@summary_bp.route('/categories', methods=['GET'])
def categories():
    """
    GET /api/summary/categories
    Optional: ?user_id=<id>
    Returns: category-wise income/expense breakdown
    Role: analyst, admin
    """
    role = request.headers.get('X-User-Role', 'viewer')
    if role not in ['analyst', 'admin']:
        return jsonify({'error': 'Permission denied. analyst or admin role required'}), 403

    user_id = request.args.get('user_id', type=int)
    data = get_category_breakdown(user_id)
    return jsonify({'category_breakdown': data}), 200


@summary_bp.route('/monthly', methods=['GET'])
def monthly():
    """
    GET /api/summary/monthly
    Optional: ?user_id=<id>
    Returns: monthly income, expense, net totals
    Role: analyst, admin
    """
    role = request.headers.get('X-User-Role', 'viewer')
    if role not in ['analyst', 'admin']:
        return jsonify({'error': 'Permission denied. analyst or admin role required'}), 403

    user_id = request.args.get('user_id', type=int)
    data = get_monthly_totals(user_id)
    return jsonify({'monthly_totals': data}), 200


@summary_bp.route('/recent', methods=['GET'])
def recent():
    """
    GET /api/summary/recent
    Optional: ?user_id=<id>&limit=<n>
    Returns: last N transactions
    """
    user_id = request.args.get('user_id', type=int)
    limit = request.args.get('limit', default=5, type=int)
    if limit > 50:
        limit = 50  # cap to prevent abuse
    data = get_recent_activity(user_id, limit)
    return jsonify({'recent_activity': data}), 200
