"""add user table

Revision ID: 0756a11e1b3d
Revises: 1313a0595333
Create Date: 2024-06-17 23:19:59.808708

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0756a11e1b3d'
down_revision = '1313a0595333'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',  # type: ignore
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email'))


def downgrade():
    op.drop_table('users')  # type: ignore
