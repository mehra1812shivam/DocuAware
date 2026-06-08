import uuid
from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, Enum, String, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.enums import Department, UserRole
from app.db.base import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(
    String(100),
    nullable=False
    )
    email: Mapped[str] = mapped_column(
    String(255),
    unique=True,
    index=True,
    nullable=False
    )
    hashed_password: Mapped[str] = mapped_column(
    String(255),
    nullable=False
    )
    department: Mapped[Department] = mapped_column(
    Enum(Department),
    nullable=False
    )
    role: Mapped[UserRole] = mapped_column(
    Enum(UserRole),
    nullable=False,
    default=UserRole.USER
    )

    is_active: Mapped[bool] = mapped_column(
    Boolean,
    nullable=False,
    default=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc)
    )

    documents: Mapped[list["Document"]] = relationship(
    back_populates="owner"
    )