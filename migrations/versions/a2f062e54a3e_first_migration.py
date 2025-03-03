"""first migration

Revision ID: a2f062e54a3e
Revises: 
Create Date: 2025-03-03 21:58:42.864197

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'a2f062e54a3e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('request',
        sa.Column('id', sa.Integer(), nullable=False),
        # ...
    )
    op.create_table('scanned',
        sa.Column('id', sa.Integer(), nullable=False),
        # ...
    )


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('documents',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('filename', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.Column('file_url', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.Column('vendor_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['vendor_id'], ['vendors.id'], name='documents_vendor_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='documents_pkey')
    )
    op.create_table('user',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    sa.Column('email', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    sa.Column('phone_number', sa.VARCHAR(length=20), autoincrement=False, nullable=False),
    sa.Column('role_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('password', sa.VARCHAR(length=120), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], name='user_role_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='user_pkey'),
    sa.UniqueConstraint('email', name='user_email_key'),
    sa.UniqueConstraint('phone_number', name='user_phone_number_key')
    )
    op.create_table('roles',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(length=50), autoincrement=False, nullable=False),
    sa.Column('permissions', postgresql.ARRAY(sa.VARCHAR()), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='roles_pkey'),
    sa.UniqueConstraint('name', name='roles_name_key')
    )
    op.create_table('vendors',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.Column('email', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.Column('phone', sa.VARCHAR(length=20), autoincrement=False, nullable=False),
    sa.Column('address', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('postal_code', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('county', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.Column('country', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.Column('kra_pin', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.Column('bank_name', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.Column('account_number', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.Column('mpesa_number', sa.VARCHAR(length=20), autoincrement=False, nullable=True),
    sa.Column('is_active', sa.BOOLEAN(), server_default=sa.text('false'), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='vendors_pkey'),
    sa.UniqueConstraint('email', name='vendors_email_key')
    )
    op.create_table('assignment',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('assignment_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('asset_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('location_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('assigned_to', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.Column('assigned_date', sa.DATE(), autoincrement=False, nullable=True),
    sa.Column('return_date', sa.DATE(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['location_id'], ['location.id'], name='assignment_location_id_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name='assignment_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('location',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('location_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.Column('description', sa.VARCHAR(length=500), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='location_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('received',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('order_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('received_quantity', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('date_received', sa.DATE(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['order_id'], ['orders.id'], name='fk_order', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name='received_pkey')
    )
    op.create_table('asset',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('item', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.Column('specifications', sa.VARCHAR(length=500), autoincrement=False, nullable=True),
    sa.Column('class_code', sa.VARCHAR(length=50), autoincrement=False, nullable=True),
    sa.Column('serial_no', sa.VARCHAR(length=50), autoincrement=False, nullable=True),
    sa.Column('assignment_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('depreciation_rate', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('purchase_price', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('depreciation_start_date', sa.DATE(), autoincrement=False, nullable=True),
    sa.Column('depreciation_end_date', sa.DATE(), autoincrement=False, nullable=True),
    sa.Column('purchase_date', sa.DATE(), autoincrement=False, nullable=True),
    sa.Column('location_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('vendor', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('condition', sa.VARCHAR(length=50), autoincrement=False, nullable=True),
    sa.Column('status', sa.VARCHAR(length=50), server_default=sa.text("'unassigned'::character varying"), autoincrement=False, nullable=True),
    sa.Column('date_returned', sa.DATE(), autoincrement=False, nullable=True),
    sa.Column('assigned_to', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['assignment_id'], ['assignment.id'], name='asset_assignment_id_fkey', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['location_id'], ['location.id'], name='asset_location_id_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name='asset_pkey'),
    sa.UniqueConstraint('serial_no', name='asset_serial_no_key')
    )
    op.create_table('orders',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('order_name', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
    sa.Column('order_description', sa.VARCHAR(length=250), autoincrement=False, nullable=True),
    sa.Column('name', sa.VARCHAR(length=50), autoincrement=False, nullable=False),
    sa.Column('cost', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False),
    sa.Column('space', sa.VARCHAR(length=50), autoincrement=False, nullable=True),
    sa.Column('vat', sa.DOUBLE_PRECISION(precision=53), server_default=sa.text('0'), autoincrement=False, nullable=True),
    sa.Column('quantity', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('status', sa.VARCHAR(length=50), autoincrement=False, nullable=False),
    sa.Column('date_ordered', sa.DATE(), autoincrement=False, nullable=False),
    sa.Column('payment_status', sa.VARCHAR(length=50), autoincrement=False, nullable=True),
    sa.Column('dispatch_status', sa.VARCHAR(length=50), autoincrement=False, nullable=True),
    sa.Column('delivery_charges', sa.DOUBLE_PRECISION(precision=53), server_default=sa.text('0'), autoincrement=False, nullable=True),
    sa.Column('reason', sa.VARCHAR(length=50), autoincrement=False, nullable=True),
    sa.Column('initialiser', sa.VARCHAR(length=50), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='orders_pkey')
    )
    op.drop_table('scanned')
    op.drop_table('request')
    # ### end Alembic commands ###
