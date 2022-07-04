"""initial

Revision ID: 99df0ce802cc
Revises: 
Create Date: 2022-07-01 21:11:59.621642

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '99df0ce802cc'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('groups',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('comment', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('permissions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('comment', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name'),
    sa.UniqueConstraint('name', name='uc_permissions_name')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=50), nullable=False),
    sa.Column('hashed_password', sa.String(length=255), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=True),
    sa.Column('first_name', sa.String(length=255), nullable=True),
    sa.Column('last_name', sa.String(length=255), nullable=True),
    sa.Column('midl_name', sa.String(length=255), nullable=True),
    sa.Column('is_superuser', sa.Boolean(), nullable=True),
    sa.Column('is_staff', sa.Boolean(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('joined_date', sa.DateTime(), nullable=True),
    sa.Column('last_login_date', sa.DateTime(), nullable=True),
    sa.Column('comment', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('hashed_password'),
    sa.UniqueConstraint('username')
    )
    op.create_table('groups_permissions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('permission', sa.Integer(), nullable=True),
    sa.Column('group', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['group'], ['groups.id'], name='fk_groups_permissions_groups_group_id', onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['permission'], ['permissions.id'], name='fk_groups_permissions_permissions_permission_id', onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users_groups',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('group', sa.Integer(), nullable=True),
    sa.Column('user', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['group'], ['groups.id'], name='fk_users_groups_groups_group_id', onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user'], ['users.id'], name='fk_users_groups_users_user_id', onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users_groups')
    op.drop_table('groups_permissions')
    op.drop_table('users')
    op.drop_table('permissions')
    op.drop_table('groups')
    # ### end Alembic commands ###