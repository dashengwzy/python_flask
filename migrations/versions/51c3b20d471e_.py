"""empty message

Revision ID: 51c3b20d471e
Revises: 43d655f3c401
Create Date: 2019-04-05 14:50:28.764152

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '51c3b20d471e'
down_revision = '43d655f3c401'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('marine_organism', sa.Column('data_set_abstract', sa.String(length=100), nullable=False))
    op.add_column('marine_organism', sa.Column('data_set_loc', sa.String(length=100), nullable=False))
    op.add_column('marine_organism', sa.Column('data_set_time_frame', sa.String(length=100), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('marine_organism', 'data_set_time_frame')
    op.drop_column('marine_organism', 'data_set_loc')
    op.drop_column('marine_organism', 'data_set_abstract')
    # ### end Alembic commands ###
