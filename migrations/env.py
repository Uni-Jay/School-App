from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

from app import create_app  # Import your factory
from app.extensions import db
from app.models import User  # Import your models to ensure they're registered
from app.models import School  # Import your models to ensure they're registered
from app.models import SchoolAdmin  # Import your models to ensure they're registered
from app.models import Course  # Import your models to ensure they're registered
from app.models import Role  # Import your models to ensure they're registered

# Setup Alembic config
config = context.config
fileConfig(config.config_file_name)

# Create the Flask app
app = create_app()

def get_metadata():
    return db.metadata

def run_migrations_online():
    with app.app_context():
        connectable = db.engine
        context.configure(
            connection=connectable.connect(),
            target_metadata=get_metadata(),
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    context.configure(
        url=app.config["SQLALCHEMY_DATABASE_URI"],
        target_metadata=get_metadata(),
        literal_binds=True,
    )

    with context.begin_transaction():
        context.run_migrations()
else:
    run_migrations_online()
