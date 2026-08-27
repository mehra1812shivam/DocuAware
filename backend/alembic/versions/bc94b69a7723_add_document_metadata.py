"""add document metadata

Revision ID: bc94b69a7723
Revises: 7b304fa31eea
Create Date: 2026-06-10 07:47:05.048643

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "bc94b69a7723"
down_revision: Union[str, Sequence[str], None] = "7b304fa31eea"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    confidentiality_enum = sa.Enum(
        "PUBLIC",
        "INTERNAL",
        "CONFIDENTIAL",
        name="confidentialitylevel",
    )

    confidentiality_enum.create(
        op.get_bind(),
        checkfirst=True,
    )

    op.add_column(
        "documents",
        sa.Column(
            "department",
            sa.Enum(
                "ENGINEERING",
                "HR",
                "FINANCE",
                "LEGAL",
                "OPERATIONS",
                "OTHER",
                name="department",
                create_type=False,
            ),
            nullable=False,
        ),
    )

    op.add_column(
        "documents",
        sa.Column(
            "confidentiality",
            sa.Enum(
                "PUBLIC",
                "INTERNAL",
                "CONFIDENTIAL",
                name="confidentialitylevel",
                create_type=False,
            ),
            nullable=False,
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_column("documents", "confidentiality")
    op.drop_column("documents", "department")

    sa.Enum(
        "PUBLIC",
        "INTERNAL",
        "CONFIDENTIAL",
        name="confidentialitylevel",
    ).drop(
        op.get_bind(),
        checkfirst=True,
    )