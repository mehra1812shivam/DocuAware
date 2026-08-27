"""add document status

Revision ID: 55ecd55aaba3
Revises: 907fd9246a16
Create Date: 2026-06-08 08:14:34.739369

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "55ecd55aaba3"
down_revision: Union[str, Sequence[str], None] = "907fd9246a16"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    document_status_enum = sa.Enum(
        "PROCESSING",
        "READY",
        "FAILED",
        name="documentstatus",
    )

    document_status_enum.create(
        op.get_bind(),
        checkfirst=True,
    )

    op.add_column(
        "documents",
        sa.Column(
            "status",
            sa.Enum(
                "PROCESSING",
                "READY",
                "FAILED",
                name="documentstatus",
                create_type=False,
            ),
            nullable=False,
            server_default="PROCESSING",
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_column("documents", "status")

    sa.Enum(
        "PROCESSING",
        "READY",
        "FAILED",
        name="documentstatus",
    ).drop(
        op.get_bind(),
        checkfirst=True,
    )