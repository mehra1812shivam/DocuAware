from sqlalchemy.orm import Session
from app.models.document import Document
from app.core.enums import  (
    DocumentStatus,
    Department,
    ConfidentialityLevel
)
from uuid import UUID
from app.utils.file_utils import get_file_type

class DocumentService:

    def __init__(self, db: Session):
        self.db = db
    def create_document(self,filename: str,owner_id: UUID,department: Department,confidentiality: ConfidentialityLevel) -> Document:
        file_type = get_file_type(filename)

        document = Document(
            filename=filename,
            file_type=file_type,
            owner_id=owner_id,
            status=DocumentStatus.PROCESSING,
            department=department,
            confidentiality=confidentiality
        )

        self.db.add(document)
        self.db.commit()
        self.db.refresh(document)

        return document
    
    def update_status(self,document_id: UUID,status: DocumentStatus)->Document:
        document = self.db.get(Document, document_id)

        if not document:
            raise ValueError("Document not found")

        document.status = status

        self.db.commit()
        self.db.refresh(document)

        return document        

    def get_documents_by_owner(self,owner_id: UUID) -> list[Document]:

        return (
            self.db.query(Document)
            .filter(Document.owner_id == owner_id)
            .order_by(Document.created_at.desc())
            .all()
        )