"""empty message

Revision ID: 276b4dff82ef
Revises: d4b0eaf305a2
Create Date: 2019-04-07 17:19:15.061558

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '276b4dff82ef'
down_revision = 'd4b0eaf305a2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('article',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('type', sa.String(length=100), nullable=False),
    sa.Column('time', sa.DateTime(), nullable=False),
    sa.Column('source', sa.Text(), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('article')
    # ### end Alembic commands ###
