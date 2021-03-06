"""empty message

Revision ID: 5962ef4cce03
Revises: 72833dc66fce
Create Date: 2018-07-02 19:52:13.504233

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "5962ef4cce03"
down_revision = "72833dc66fce"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "ride_riders",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.Column("ride_id", sa.Integer(), nullable=True),
        sa.Column("rider_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["ride_id"], ["rides.id"]),
        sa.ForeignKeyConstraint(["rider_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("ride_riders")
    # ### end Alembic commands ###
