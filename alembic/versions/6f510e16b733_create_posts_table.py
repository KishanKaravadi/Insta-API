"""create posts table

Revision ID: 6f510e16b733
Revises: 
Create Date: 2024-06-17 23:00:53.764132

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6f510e16b733'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts', sa.Column(  # type: ignore
        'id', sa.Integer, nullable=False, primary_key=True), sa.Column('title', sa.String, nullable=False))


def downgrade():
    op.drop_table('posts')  # type: ignore
