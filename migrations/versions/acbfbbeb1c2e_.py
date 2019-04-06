"""empty message

Revision ID: acbfbbeb1c2e
Revises: c08cb127ce56
Create Date: 2019-04-06 11:03:25.321405

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'acbfbbeb1c2e'
down_revision = 'c08cb127ce56'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('marine_hydrology',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('route', sa.String(length=100), nullable=False),
    sa.Column('data_set_name', sa.String(length=100), nullable=False),
    sa.Column('data_set_size', sa.String(length=100), nullable=False),
    sa.Column('data_set_source', sa.String(length=1000), nullable=False),
    sa.Column('data_set_time_frame', sa.String(length=100), nullable=False),
    sa.Column('data_set_loc', sa.String(length=100), nullable=False),
    sa.Column('data_set_abstract', sa.String(length=10000), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('marine_hydrology')
    # ### end Alembic commands ###
