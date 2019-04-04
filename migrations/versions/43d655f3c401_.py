"""empty message

Revision ID: 43d655f3c401
Revises: c53cc56b029b
Create Date: 2019-04-04 23:32:12.326539

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '43d655f3c401'
down_revision = 'c53cc56b029b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('marine_organism',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('route', sa.String(length=100), nullable=False),
    sa.Column('data_set_name', sa.String(length=100), nullable=False),
    sa.Column('data_set_size', sa.String(length=100), nullable=False),
    sa.Column('data_set_source', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('marine_organism')
    # ### end Alembic commands ###
