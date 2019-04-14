"""empty message

Revision ID: 854a5afb9ad7
Revises: 11ea31a4a7bc
Create Date: 2019-04-13 23:07:40.257589

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '854a5afb9ad7'
down_revision = '11ea31a4a7bc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('organ', sa.String(length=100), nullable=False),
    sa.Column('username', sa.String(length=100), nullable=False),
    sa.Column('password', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    # ### end Alembic commands ###