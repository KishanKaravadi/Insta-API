"""add content column to posts table

Revision ID: 1313a0595333
Revises: 6f510e16b733
Create Date: 2024-06-17 23:14:46.810736

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1313a0595333'
down_revision = '6f510e16b733'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column(  # type: ignore
        'content', sa.String, nullable=False))


def downgrade():
    op.drop_column('posts', 'content')  # type: ignore
