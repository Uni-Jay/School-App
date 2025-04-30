from flask_sqlalchemy import SQLAlchemy


from .user import User  # Import User model to ensure it's registered
from .school import School
from .school_admin import SchoolAdmin
