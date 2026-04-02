from models.user import User
from models.transaction import Transaction
from extensions import db
from datetime import date


def seed_data():
    """Seed the database with sample users and transactions if empty."""
    if User.query.first():
        return  # Already seeded

    # Create sample users
    admin = User(name='Abhay Admin', email='admin@finance.com', role='admin')
    analyst = User(name='Riya Analyst', email='riya@finance.com', role='analyst')
    viewer = User(name='Raj Viewer', email='raj@finance.com', role='viewer')

    db.session.add_all([admin, analyst, viewer])
    db.session.commit()

    # Create sample transactions for admin user
    transactions = [
        Transaction(amount=50000.0, type='income', category='Salary',
                    date=date(2025, 3, 1), notes='March salary', user_id=admin.id),
        Transaction(amount=1200.0, type='expense', category='Groceries',
                    date=date(2025, 3, 5), notes='Big Bazaar shopping', user_id=admin.id),
        Transaction(amount=800.0, type='expense', category='Transport',
                    date=date(2025, 3, 10), notes='Petrol', user_id=admin.id),
        Transaction(amount=3000.0, type='expense', category='Rent',
                    date=date(2025, 3, 1), notes='Monthly rent', user_id=admin.id),
        Transaction(amount=5000.0, type='income', category='Freelance',
                    date=date(2025, 3, 15), notes='Web project payment', user_id=analyst.id),
        Transaction(amount=500.0, type='expense', category='Entertainment',
                    date=date(2025, 3, 20), notes='Movie + dinner', user_id=analyst.id),
        Transaction(amount=50000.0, type='income', category='Salary',
                    date=date(2025, 4, 1), notes='April salary', user_id=admin.id),
        Transaction(amount=2000.0, type='expense', category='Groceries',
                    date=date(2025, 4, 7), notes='Monthly groceries', user_id=admin.id),
    ]

    db.session.add_all(transactions)
    db.session.commit()
    print("✅ Sample data seeded successfully.")
