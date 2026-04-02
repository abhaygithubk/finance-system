from extensions import db
from models.user import User, VALID_ROLES


def validate_user_data(data, is_update=False):
    if not is_update:
        required = ['name', 'email']
        for field in required:
            if not data.get(field):
                return False, f"Missing required field: '{field}'"

    if 'email' in data and data['email']:
        existing = User.query.filter_by(email=data['email']).first()
        if existing:
            return False, f"Email '{data['email']}' is already registered"

    if 'role' in data and data['role'] not in VALID_ROLES:
        return False, f"Role must be one of: {', '.join(VALID_ROLES)}"

    return True, None


def create_user(data):
    user = User(
        name=data['name'].strip(),
        email=data['email'].strip().lower(),
        role=data.get('role', 'viewer')
    )
    db.session.add(user)
    db.session.commit()
    return user


def get_all_users():
    return User.query.all()


def get_user_by_id(user_id):
    return User.query.get(user_id)


def update_user(user, data, requesting_role):
    """Only admin can update roles."""
    if 'name' in data:
        user.name = data['name'].strip()

    if 'role' in data:
        if requesting_role != 'admin':
            return None, "Only admins can change user roles"
        if data['role'] not in VALID_ROLES:
            return None, f"Role must be one of: {', '.join(VALID_ROLES)}"
        user.role = data['role']

    db.session.commit()
    return user, None


def delete_user(user, requesting_role):
    if requesting_role != 'admin':
        return False, "Only admins can delete users"
    db.session.delete(user)
    db.session.commit()
    return True, None
