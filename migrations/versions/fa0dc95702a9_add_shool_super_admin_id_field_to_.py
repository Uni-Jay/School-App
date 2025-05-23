"""Add shool_super_admin_id field to Course model

Revision ID: fa0dc95702a9
Revises: 32a40c202cab
Create Date: 2025-05-01 13:02:38.002114

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fa0dc95702a9'
down_revision = '32a40c202cab'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('course', sa.Column('school_super_admin_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'course', 'user', ['school_super_admin_id'], ['id'])
    op.create_foreign_key(None, 'course', 'school', ['school_id'], ['id'])
    op.create_foreign_key(None, 'school_admin', 'school', ['school_id'], ['id'])
    op.create_foreign_key(None, 'school_admin', 'user', ['school_super_admin_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'school_admin', type_='foreignkey')
    op.drop_constraint(None, 'school_admin', type_='foreignkey')
    op.drop_constraint(None, 'course', type_='foreignkey')
    op.drop_constraint(None, 'course', type_='foreignkey')
    op.drop_column('course', 'school_super_admin_id')
    # ### end Alembic commands ###
