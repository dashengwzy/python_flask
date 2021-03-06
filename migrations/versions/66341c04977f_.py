"""empty message

Revision ID: 66341c04977f
Revises: 3326ec05d68b
Create Date: 2019-04-09 18:08:37.626834

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '66341c04977f'
down_revision = '3326ec05d68b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('data', sa.Column('class_name', sa.String(length=100), nullable=False))
    op.add_column('data', sa.Column('in_id', sa.Integer(), nullable=False))
    op.drop_column('data', 'data_route')
    op.drop_column('data', 'data_name')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('data', sa.Column('data_name', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False))
    op.add_column('data', sa.Column('data_route', mysql.VARCHAR(length=100), nullable=False))
    op.drop_column('data', 'in_id')
    op.drop_column('data', 'class_name')
    # ### end Alembic commands ###
