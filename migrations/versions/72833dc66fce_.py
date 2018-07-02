"""empty message

Revision ID: 72833dc66fce
Revises: d36c6cda5a72
Create Date: 2018-07-02 14:24:41.220764

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '72833dc66fce'
down_revision = 'd36c6cda5a72'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('rides_user_id_fkey', 'rides', type_='foreignkey')
    op.drop_column('rides', 'user_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('rides', sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.create_foreign_key('rides_user_id_fkey', 'rides', 'users', ['user_id'], ['id'])
    # ### end Alembic commands ###
