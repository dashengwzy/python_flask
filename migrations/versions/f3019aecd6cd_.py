"""empty message

Revision ID: f3019aecd6cd
Revises: 276b4dff82ef
Create Date: 2019-04-08 14:50:42.795977

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f3019aecd6cd'
down_revision = '276b4dff82ef'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('marine_chemistry',
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
    op.create_table('chemistry_data',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('data_route', sa.String(length=100), nullable=False),
    sa.Column('data_name', sa.String(length=100), nullable=False),
    sa.Column('data_time', sa.DateTime(), nullable=False),
    sa.Column('data_format', sa.String(length=100), nullable=False),
    sa.Column('data_kind', sa.String(length=100), nullable=False),
    sa.Column('data_refresh', sa.String(length=100), nullable=False),
    sa.Column('uid_hydrology', sa.Integer(), nullable=True),
    sa.Column('down_time', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['uid_hydrology'], ['marine_chemistry.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('chemistry_data')
    op.drop_table('marine_chemistry')
    # ### end Alembic commands ###