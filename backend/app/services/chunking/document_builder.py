from langchain_core.documents import Document

from app.models.document import Document as DbDocument


class DocumentBuilder:

    def build(
        self,
        chunks: list[str],
        document: DbDocument
    ) -> list[Document]:

        documents = []

        for chunk in chunks:

            documents.append(
                Document(
                    page_content=chunk,
                    metadata={
                        "document_id": str(document.id),
                        "owner_id": str(document.owner_id),
                        "department": document.department.value,
                        "confidentiality": document.confidentiality.value,
                        "filename": document.filename
                    }
                )
            )

        return documents