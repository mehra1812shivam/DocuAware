"""create users table

Revision ID: 4c4208a5ffe1
Revises:
Create Date: 2026-06-04 08:49:30.452744

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "4c4208a5ffe1"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.create_table(
        "users",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("hashed_password", sa.String(length=255), nullable=False),
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
            ),
            nullable=False,
        ),
        sa.Column(
            "role",
            sa.Enum(
                "USER",
                "ADMIN",
                name="userrole",
            ),
            nullable=False,
        ),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        op.f("ix_users_email"),
        "users",
        ["email"],
        unique=True,
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_index(
        op.f("ix_users_email"),
        table_name="users",
    )

    op.drop_table("users")

    # PostgreSQL enum types are created by the table migration,
    # so remove them when downgrading.
    sa.Enum(
        "USER",
        "ADMIN",
        name="userrole",
    ).drop(op.get_bind(), checkfirst=True)

    sa.Enum(
        "ENGINEERING",
        "HR",
        "FINANCE",
        "LEGAL",
        "OPERATIONS",
        "OTHER",
        name="department",
    ).drop(op.get_bind(), checkfirst=True)