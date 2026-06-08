from sqlalchemy.orm import Session
from app.models.document import Document
from app.core.enums import  DocumentStatus
from uuid import UUID
from app.utils.file_utils import get_file_type

class DocumentService:

    def __init__(self, db: Session):
        self.db = db
    def create_document(self,filename: str,owner_id: UUID) -> Document:
        file_type = get_file_type(filename)

        document = Document(
            filename=filename,
            file_type=file_type,
            owner_id=owner_id,
            status=DocumentStatus.PROCESSING
        )

        self.db.add(document)
        self.db.commit()
        self.db.refresh(document)

        return document