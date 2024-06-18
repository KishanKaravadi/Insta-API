"""add last few columns to post table

Revision ID: 938668f9aebb
Revises: b67eaae424b4
Create Date: 2024-06-17 23:41:05.433452

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '938668f9aebb'
down_revision = 'b67eaae424b4'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('published',  # type: ignore
                                     sa.Boolean(), server_default='TRUE', nullable=False))
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True),  # type: ignore
                                     nullable=False, server_default=sa.text('now()'))
                  )


def downgrade():
    op.drop_column('posts', 'published')  # type: ignore
    op.drop_column('posts', 'created_at')  # type: ignore
