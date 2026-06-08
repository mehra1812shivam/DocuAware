import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, String, UUID, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.enums import DocumentStatus,FileType
from app.db.base import Base


class Document(Base):
    __tablename__ = "documents"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    filename: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    file_type: Mapped[FileType] = mapped_column(
    Enum(FileType),
    nullable=False
    )

    owner_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False
    )

    status: Mapped[DocumentStatus] = mapped_column(
    Enum(DocumentStatus),
    nullable=False,
    default=DocumentStatus.PROCESSING
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc)
    )

    owner: Mapped["User"] = relationship(
    back_populates="documents"
    )