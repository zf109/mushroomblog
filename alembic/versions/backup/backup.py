"""empty message

Revision ID: eb11030a3259
Revises: 
Create Date: 2019-06-02 13:00:30.469435

"""
from alembic import op
import sqlalchemy as sa

from mushroom.config import Config as conf

# revision identifiers, used by Alembic.
# revision = 'eb11030a3259'
# down_revision = None
# branch_labels = None
# depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute(f'CREATE SCHEMA {conf.SCHEMA}')
    op.create_table('user',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('password', sa.String(length=128), nullable=True),
    sa.Column('nickname', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    schema='mushroom'
    )
    op.create_index(op.f('ix_mushroom_user_email'), 'user', ['email'], unique=True, schema='mushroom')
    op.create_index(op.f('ix_mushroom_user_nickname'), 'user', ['nickname'], unique=True, schema='mushroom')
    op.create_index(op.f('ix_mushroom_user_username'), 'user', ['username'], unique=True, schema='mushroom')
    op.create_table('post',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('title', sa.String(length=140), nullable=True),
    sa.Column('body', sa.String(), nullable=True),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.Column('last_modified', sa.DateTime(), nullable=True),
    sa.Column('like_count', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['mushroom.user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    schema='mushroom'
    )
    op.create_table('comment',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('body', sa.String(), nullable=True),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.Column('last_modified', sa.DateTime(), nullable=True),
    sa.Column('like_count', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.String(length=36), nullable=True),
    sa.Column('post_id', sa.String(length=36), nullable=True),
    sa.ForeignKeyConstraint(['post_id'], ['mushroom.post.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['mushroom.user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    schema='mushroom'
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    
    op.drop_table('comment', schema='mushroom')
    op.drop_table('post', schema='mushroom')
    op.drop_index(op.f('ix_mushroom_user_username'), table_name='user', schema='mushroom')
    op.drop_index(op.f('ix_mushroom_user_nickname'), table_name='user', schema='mushroom')
    op.drop_index(op.f('ix_mushroom_user_email'), table_name='user', schema='mushroom')
    op.drop_table('user', schema='mushroom')

    op.execute(f'DROP SCHEMA {conf.SCHEMA}')
    # ### end Alembic commands ###
