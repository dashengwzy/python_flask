"""empty message

Revision ID: e16394682414
Revises: 
Create Date: 2019-04-03 15:29:35.347570

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e16394682414'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('banner',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('route', sa.String(length=100), nullable=False),
    sa.Column('main_title', sa.String(length=100), nullable=False),
    sa.Column('vice_title_one', sa.String(length=100), nullable=False),
    sa.Column('vice_title_two', sa.String(length=100), nullable=False),
    sa.Column('button_font', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('banner')
    # ### end Alembic commands ###
