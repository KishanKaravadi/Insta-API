"""add foreign key to posts table

Revision ID: b67eaae424b4
Revises: 0756a11e1b3d
Create Date: 2024-06-17 23:30:56.507425

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b67eaae424b4'
down_revision = '0756a11e1b3d'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column(  # type: ignore
        'owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_user_fk', source_table='posts', referent_table='users', local_cols=[  # type: ignore
                          'owner_id'], remote_cols=['id'], ondelete="CASCADE")


def downgrade():
    op.drop_constraint('post_users_fk', table_name='posts')  # type: ignore
    op.drop_column('posts', 'owner_id')  # type: ignore
