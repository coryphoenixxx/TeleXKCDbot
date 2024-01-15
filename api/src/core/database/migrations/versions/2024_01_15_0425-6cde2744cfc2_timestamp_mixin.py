"""Timestamp mixin

Revision ID: 6cde2744cfc2
Revises: a2b881ae0485
Create Date: 2024-01-15 04:25:02.288588

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "6cde2744cfc2"
down_revision = "a2b881ae0485"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "comics",
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    )
    op.add_column(
        "translation_images",
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    )
    op.add_column(
        "translations",
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    )
    op.add_column(
        "translations",
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("translations", "updated_at")
    op.drop_column("translations", "created_at")
    op.drop_column("translation_images", "updated_at")
    op.drop_column("comics", "updated_at")
    # ### end Alembic commands ###
