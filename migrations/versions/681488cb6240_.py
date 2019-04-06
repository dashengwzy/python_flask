"""empty message

Revision ID: 681488cb6240
Revises: 64dd8fd9582b
Create Date: 2019-04-05 16:21:10.350766

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '681488cb6240'
down_revision = '64dd8fd9582b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('organism_data', sa.Column('organism_data_format', sa.String(length=100), nullable=False))
    op.add_column('organism_data', sa.Column('organism_data_name', sa.String(length=100), nullable=False))
    op.add_column('organism_data', sa.Column('organism_data_self', sa.Text(), nullable=False))
    op.add_column('organism_data', sa.Column('organism_data_time', sa.DateTime(), nullable=False))
    op.drop_column('organism_data', 'route')
    op.drop_column('organism_data', 'data_set_name')
    op.drop_column('organism_data', 'data_set_size')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('organism_data', sa.Column('data_set_size', mysql.VARCHAR(length=100), nullable=False))
    op.add_column('organism_data', sa.Column('data_set_name', mysql.DATETIME(), nullable=False))
    op.add_column('organism_data', sa.Column('route', mysql.VARCHAR(length=100), nullable=False))
    op.drop_column('organism_data', 'organism_data_time')
    op.drop_column('organism_data', 'organism_data_self')
    op.drop_column('organism_data', 'organism_data_name')
    op.drop_column('organism_data', 'organism_data_format')
    # ### end Alembic commands ###