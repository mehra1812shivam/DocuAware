"""add file type

Revision ID: 7b304fa31eea
Revises: 55ecd55aaba3
Create Date: 2026-06-08 08:27:45.364575

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "7b304fa31eea"
down_revision: Union[str, Sequence[str], None] = "55ecd55aaba3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    file_type_enum = sa.Enum(
        "PDF",
        "DOCX",
        "TXT",
        name="filetype",
    )

    file_type_enum.create(
        op.get_bind(),
        checkfirst=True,
    )

    op.add_column(
        "documents",
        sa.Column(
            "file_type",
            sa.Enum(
                "PDF",
                "DOCX",
                "TXT",
                name="filetype",
                create_type=False,
            ),
            nullable=False,
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_column("documents", "file_type")

    sa.Enum(
        "PDF",
        "DOCX",
        "TXT",
        name="filetype",
    ).drop(
        op.get_bind(),
        checkfirst=True,
    )