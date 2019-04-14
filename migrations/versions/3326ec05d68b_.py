"""empty message

Revision ID: 3326ec05d68b
Revises: 57d2a0de8607
Create Date: 2019-04-09 18:07:27.831378

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3326ec05d68b'
down_revision = '57d2a0de8607'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('data',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('data_route', sa.String(length=100), nullable=False),
    sa.Column('data_name', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('data')
    # ### end Alembic commands ###