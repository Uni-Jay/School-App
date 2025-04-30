# app/__init__.py
from flask import Flask
from app.config import Config
from app.extensions import db, migrate, jwt
from dotenv import load_dotenv
load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # Import routes and register blueprints AFTER extensions
    from app.auth.auth_routes import auth
    app.register_blueprint(auth, url_prefix='/auth')
    from app.routes.school_routes import school_bp
    app.register_blueprint(school_bp)
    from app.routes.school_admin_routes import school_admin_bp
    app.register_blueprint(school_admin_bp)

    return app
