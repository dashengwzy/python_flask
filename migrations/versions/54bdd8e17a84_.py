"""empty message

Revision ID: 54bdd8e17a84
Revises: 66341c04977f
Create Date: 2019-04-09 18:22:32.043127

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '54bdd8e17a84'
down_revision = '66341c04977f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('data', 'class_name')
    op.drop_column('data', 'in_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('data', sa.Column('in_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False))
    op.add_column('data', sa.Column('class_name', mysql.VARCHAR(length=100), nullable=False))
    # ### end Alembic commands ###
