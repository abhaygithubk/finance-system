from models.transaction import Transaction
from sqlalchemy import func
from extensions import db
from datetime import datetime


def get_summary(user_id=None):
    """Returns total income, total expense, current balance."""
    query = Transaction.query
    if user_id:
        query = query.filter_by(user_id=user_id)

    transactions = query.all()

    total_income = sum(t.amount for t in transactions if t.type == 'income')
    total_expense = sum(t.amount for t in transactions if t.type == 'expense')
    balance = total_income - total_expense

    return {
        'total_income': round(total_income, 2),
        'total_expenses': round(total_expense, 2),
        'current_balance': round(balance, 2),
        'total_transactions': len(transactions)
    }


def get_category_breakdown(user_id=None):
    """Returns expense breakdown by category."""
    query = db.session.query(
        Transaction.category,
        Transaction.type,
        func.sum(Transaction.amount).label('total')
    )
    if user_id:
        query = query.filter(Transaction.user_id == user_id)

    results = query.group_by(Transaction.category, Transaction.type).all()

    breakdown = {}
    for row in results:
        key = f"{row.category} ({row.type})"
        breakdown[key] = round(row.total, 2)

    return breakdown


def get_monthly_totals(user_id=None):
    """Returns monthly income and expense totals."""
    query = Transaction.query
    if user_id:
        query = query.filter_by(user_id=user_id)

    transactions = query.all()

    monthly = {}
    for t in transactions:
        month_key = t.date.strftime('%Y-%m')
        if month_key not in monthly:
            monthly[month_key] = {'income': 0.0, 'expense': 0.0}
        monthly[month_key][t.type] += t.amount

    # Round values
    for month in monthly:
        monthly[month]['income'] = round(monthly[month]['income'], 2)
        monthly[month]['expense'] = round(monthly[month]['expense'], 2)
        monthly[month]['net'] = round(
            monthly[month]['income'] - monthly[month]['expense'], 2
        )

    return dict(sorted(monthly.items(), reverse=True))


def get_recent_activity(user_id=None, limit=5):
    """Returns the most recent transactions."""
    query = Transaction.query
    if user_id:
        query = query.filter_by(user_id=user_id)

    recent = query.order_by(Transaction.created_at.desc()).limit(limit).all()
    return [t.to_dict() for t in recent]
