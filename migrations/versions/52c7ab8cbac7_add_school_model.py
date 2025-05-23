"""Add School model

Revision ID: 52c7ab8cbac7
Revises: 437edf1baede
Create Date: 2025-04-30 18:17:27.964820

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '52c7ab8cbac7'
down_revision = '437edf1baede'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('school',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('school_name', sa.String(length=120), nullable=False),
    sa.Column('school_email', sa.String(length=120), nullable=False),
    sa.Column('school_phone_number', sa.String(length=20), nullable=False),
    sa.Column('school_image', sa.String(length=255), nullable=True),
    sa.Column('school_address', sa.Text(), nullable=False),
    sa.Column('school_type', sa.String(length=20), nullable=False),
    sa.Column('school_registration_date', sa.Date(), nullable=True),
    sa.Column('school_registration_number', sa.String(length=100), nullable=True),
    sa.Column('school_csc_number', sa.String(length=100), nullable=True),
    sa.Column('school_website', sa.String(length=255), nullable=True),
    sa.Column('school_social_media', sa.String(length=255), nullable=True),
    sa.Column('school_super_admin_id', sa.Integer(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('school_email')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('school')
    # ### end Alembic commands ###
