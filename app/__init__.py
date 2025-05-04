# app/__init__.py
from flask import Flask
from app.config import Config
from app.extensions import db, migrate, jwt
from flask_cors import CORS
from dotenv import load_dotenv
from flask import send_from_directory
load_dotenv()



def create_app():

    # @app.route('/static/uploads/<filename>')
    # def uploaded_file(filename):
    #     return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(Config)


        
  

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # Import routes and register blueprints AFTER extensions
    from app.auth.auth_routes import auth_bp
    app.register_blueprint(auth_bp)
    from app.routes.school_routes import school_bp
    app.register_blueprint(school_bp)
    from app.routes.school_admin_routes import school_admin_bp
    app.register_blueprint(school_admin_bp)
    from app.routes.course_routes import course_bp
    app.register_blueprint(course_bp)
    from app.routes.user_routes import user_bp
    app.register_blueprint(user_bp)

    return app
