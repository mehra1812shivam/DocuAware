from sqlalchemy.orm import Session
from uuid import UUID
from app.models.document import Document
from app.core.enums import ConfidentialityLevel
from app.services.vector_stores.qdrant_service import QdrantService
from app.services.llm.gemini_service import GeminiService


class SummaryService:

    def __init__(self):
        self.qdrant_service = QdrantService()
        self.gemini_service = GeminiService()

    def summarize(
        self,
        document_id: UUID,
        owner_id: UUID,
        department: str,
        db: Session
    ):
        document = (
            db.query(Document)
            .filter(Document.id == document_id)
            .first()
        )

        if not document:
            raise ValueError("Document not found")

        # Access check
        if str(document.owner_id) != owner_id:

            if document.confidentiality == ConfidentialityLevel.CONFIDENTIAL:
                raise PermissionError("Access denied")

            if (
                document.confidentiality == ConfidentialityLevel.INTERNAL
                and document.department.value != department
            ):
                raise PermissionError("Access denied")

        chunks = self.qdrant_service.get_document_chunks(
            document_id=str(document_id)
        )

        if not chunks:
            raise ValueError("No chunks found for document")

        # Temporary V1 implementation.
        # We'll replace this with proper batching next.
        context = "\n\n".join(
            chunk.payload["content"]
            for chunk in chunks
        )

        prompt = f"""
You are DocuAware.

Summarize the supplied document context.

Rules:
- Use ONLY the supplied context.
- Do not fabricate information.
- Preserve important facts, concepts and conclusions.
- Produce a clear, structured summary.

Document:
{document.filename}

Context:
--------
{context}
--------

Summary:
"""

        summary = self.gemini_service.generate(prompt)

        return {
            "document_id": str(document.id),
            "filename": document.filename,
            "summary": summary
        }