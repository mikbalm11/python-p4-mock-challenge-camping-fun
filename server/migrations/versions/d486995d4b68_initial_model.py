"""initial model

Revision ID: d486995d4b68
Revises: 
Create Date: 2025-05-13 22:28:19.738107

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd486995d4b68'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('activities',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('difficulty', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_activities'))
    )
    op.create_table('campers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('age', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_campers'))
    )
    op.create_table('signups',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('time', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_signups'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('signups')
    op.drop_table('campers')
    op.drop_table('activities')
    # ### end Alembic commands ###
