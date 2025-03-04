"""adds relationship btwn scanned and user tables

"""
revision = '98da04087724'
down_revision = '38eab2906006'
create_date = '2025-03-04 06:29:58.639563'

from alembic import op
import sqlalchemy as sa
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate(db=db)

def upgrade():
    # Add foreign key constraint to Scanned table
    op.create_unique_constraint('uq_scanned_id', 'scanned', ['id'])
    op.add_column('scanned', sa.Column('user_id', sa.Integer(), nullable=False))
    op.alter_column('scanned', 'id', existing_type=db.Integer(), primary_key=True, unique=True, nullable=False)
    op.create_foreign_key('fk_scanned_user', 'scanned', 'user', ['user_id'], ['id'])

    # Add relationship to User table
    op.add_column('user', sa.Column('scanned_id', sa.Integer(), nullable=True))
    op.execute('UPDATE "user" SET scanned_id = NULL WHERE scanned_id IS NULL') 
    
    op.create_foreign_key('fk_user_scanned', 'user', 'scanned', ['scanned_id'], ['id'])

def downgrade():
    # Remove foreign key constraint from Scanned table
    op.drop_constraint('fk_scanned_user', 'scanned', type_='foreignkey')
    op.drop_colCodeiumumn('scanned', 'user_id')

    # Remove relationship from User table
    op.drop_constraint('fk_user_scanned', 'user', type_='foreignkey')
    op.drop_column('user', 'scanned_id')