from functools import wraps
from flask import request, jsonify


def require_role(*allowed_roles):
    """
    Decorator to enforce role-based access control.
    Usage: @require_role('admin', 'analyst')
    Role is passed via X-User-Role request header.
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            role = request.headers.get('X-User-Role', 'viewer')
            if role not in allowed_roles:
                return jsonify({
                    'error': f'Access denied. Required role(s): {", ".join(allowed_roles)}'
                }), 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator
