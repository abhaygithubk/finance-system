from extensions import db
from models.transaction import Transaction
from models.user import User
from datetime import datetime


def validate_transaction_data(data):
    """Validate incoming transaction data. Returns (is_valid, error_message)."""
    required_fields = ['amount', 'type', 'category', 'date', 'user_id']
    for field in required_fields:
        if field not in data:
            return False, f"Missing required field: '{field}'"

    try:
        amount = float(data['amount'])
        if amount <= 0:
            return False, "Amount must be a positive number"
    except (ValueError, TypeError):
        return False, "Amount must be a valid number"

    if data['type'] not in ['income', 'expense']:
        return False, "Type must be 'income' or 'expense'"

    try:
        datetime.strptime(data['date'], '%Y-%m-%d')
    except ValueError:
        return False, "Date must be in YYYY-MM-DD format"

    user = User.query.get(data['user_id'])
    if not user:
        return False, f"User with id {data['user_id']} does not exist"

    return True, None


def create_transaction(data):
    transaction = Transaction(
        amount=float(data['amount']),
        type=data['type'],
        category=data['category'].strip(),
        date=datetime.strptime(data['date'], '%Y-%m-%d').date(),
        notes=data.get('notes', '').strip(),
        user_id=int(data['user_id'])
    )
    db.session.add(transaction)
    db.session.commit()
    return transaction


def get_all_transactions(filters=None):
    query = Transaction.query

    if filters:
        if filters.get('type'):
            query = query.filter_by(type=filters['type'])
        if filters.get('category'):
            query = query.filter_by(category=filters['category'])
        if filters.get('user_id'):
            query = query.filter_by(user_id=filters['user_id'])
        if filters.get('date_from'):
            try:
                date_from = datetime.strptime(filters['date_from'], '%Y-%m-%d').date()
                query = query.filter(Transaction.date >= date_from)
            except ValueError:
                pass
        if filters.get('date_to'):
            try:
                date_to = datetime.strptime(filters['date_to'], '%Y-%m-%d').date()
                query = query.filter(Transaction.date <= date_to)
            except ValueError:
                pass

    return query.order_by(Transaction.date.desc()).all()


def get_transaction_by_id(transaction_id):
    return Transaction.query.get(transaction_id)


def update_transaction(transaction, data):
    if 'amount' in data:
        try:
            amount = float(data['amount'])
            if amount <= 0:
                return None, "Amount must be a positive number"
            transaction.amount = amount
        except (ValueError, TypeError):
            return None, "Amount must be a valid number"

    if 'type' in data:
        if data['type'] not in ['income', 'expense']:
            return None, "Type must be 'income' or 'expense'"
        transaction.type = data['type']

    if 'category' in data:
        transaction.category = data['category'].strip()

    if 'date' in data:
        try:
            transaction.date = datetime.strptime(data['date'], '%Y-%m-%d').date()
        except ValueError:
            return None, "Date must be in YYYY-MM-DD format"

    if 'notes' in data:
        transaction.notes = data['notes'].strip()

    db.session.commit()
    return transaction, None


def delete_transaction(transaction):
    db.session.delete(transaction)
    db.session.commit()
