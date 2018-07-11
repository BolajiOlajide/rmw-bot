"""empty message

Revision ID: 9e93b9838826
Revises: 
Create Date: 2018-06-23 00:54:36.557158

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9e93b9838826'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('slack_uid', sa.String(length=50), nullable=False),
    sa.Column('slack_name', sa.String(length=80), nullable=False),
    sa.Column('full_name', sa.String(length=100), nullable=False),
    sa.Column('phone_number', sa.String(length=20), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('rides',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('driver_id', sa.Integer(), nullable=True),
    sa.Column('origin', sa.String(length=100), nullable=False),
    sa.Column('destination', sa.String(length=80), nullable=False),
    sa.Column('take_off', sa.DateTime(), nullable=False),
    sa.Column('max_seats', sa.Integer(), nullable=False),
    sa.Column('seats_left', sa.Integer(), nullable=True),
    sa.Column('status', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['driver_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('rides')
    op.drop_table('users')
    # ### end Alembic commands ###