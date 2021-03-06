"""empty message

Revision ID: c83ab55ec76c
Revises: 6ced38ceee38
Create Date: 2019-04-07 15:13:10.894748

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c83ab55ec76c'
down_revision = '6ced38ceee38'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('hydrology_data', sa.Column('uid_hydrology', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'hydrology_data', 'marine_hydrology', ['uid_hydrology'], ['id'])
    op.add_column('organism_data', sa.Column('uid_organism', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'organism_data', 'marine_organism', ['uid_organism'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'organism_data', type_='foreignkey')
    op.drop_column('organism_data', 'uid_organism')
    op.drop_constraint(None, 'hydrology_data', type_='foreignkey')
    op.drop_column('hydrology_data', 'uid_hydrology')
    # ### end Alembic commands ###
