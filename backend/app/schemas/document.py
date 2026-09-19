from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from app.core.enums import (
    ConfidentialityLevel,
    Department,
    DocumentStatus,
    FileType,
)


class DocumentResponse(BaseModel):
    id: UUID
    filename: str
    file_type: FileType
    status: DocumentStatus
    department: Department
    confidentiality: ConfidentialityLevel
    created_at: datetime
