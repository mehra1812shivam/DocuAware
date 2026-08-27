from fastapi import APIRouter, Depends, UploadFile, File
from fastapi import HTTPException
from app.models import User
from app.api.dependencies import get_current_user,get_db
from app.utils.storage import save_uploaded_file
from app.utils.file_utils import get_file_type
from app.services.extractors.selector import TextExtractorSelector
from fastapi import Form
from sqlalchemy.orm import Session
from app.core.enums import (ConfidentialityLevel,DocumentStatus)
from app.services.document_service import DocumentService
from app.schemas.document import DocumentResponse
from app.services.ingestion.document_ingestion_service import (
    DocumentIngestionService
)

router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)

@router.post("/upload")
def upload_document(
    file: UploadFile = File(...),
    confidentiality: ConfidentialityLevel = Form(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:

        file_type = get_file_type(file.filename)

        document_service = DocumentService(db)

        document = document_service.create_document(
            filename=file.filename,
            owner_id=current_user.id,
            department=current_user.department,
            confidentiality=confidentiality
        )

        file_path = save_uploaded_file(file)

        extractor = TextExtractorSelector()

        text = extractor.extract(
            file_type=file_type,
            file_path=str(file_path)
        )
        ingestion_service = DocumentIngestionService()

        ingestion_service.ingest(
            text=text,
            document=document
        )

        document_service.update_status(
            document.id,
            DocumentStatus.READY
        )        

        return {
            "message": "File uploaded successfully",
            "document_id": str(document.id),
            "filename": file.filename,
            "status": DocumentStatus.READY.value,
            "text_preview": text[:500]
        }

    except Exception as e:

        if 'document' in locals():
            document_service.update_status(
            document.id,
            DocumentStatus.FAILED
        )

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

@router.get("", response_model=list[DocumentResponse])
def get_documents(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    document_service = DocumentService(db)

    return document_service.get_accessible_documents(
        current_user
    )