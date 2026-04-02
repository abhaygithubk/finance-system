from flask import Flask
from config import Config
from extensions import db
from routes.transactions import transactions_bp
from routes.summary import summary_bp
from routes.users import users_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    # Register Blueprints
    app.register_blueprint(transactions_bp, url_prefix='/api/transactions')
    app.register_blueprint(summary_bp, url_prefix='/api/summary')
    app.register_blueprint(users_bp, url_prefix='/api/users')

    with app.app_context():
        db.create_all()
        from utils.seed import seed_data
        seed_data()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
