from app.services.chunking.text_chunker import TextChunker
from app.services.chunking.document_builder import DocumentBuilder
from app.services.embeddings.embedding_service import EmbeddingService
from app.services.vector_stores.qdrant_service import QdrantService
from app.models.document import Document as DbDocument

class DocumentIngestionService:

    def __init__(self):

        self.chunker = TextChunker()
        self.document_builder = DocumentBuilder()
        self.embedding_service = EmbeddingService()
        self.qdrant_service = QdrantService()
    def ingest(self,text: str,document: DbDocument):

        chunks = self.chunker.split(text)

        documents = self.document_builder.build(
            chunks=chunks,
            document=document
        )

        embeddings = self.embedding_service.embed(
            [doc.page_content for doc in documents]
        )

        self.qdrant_service.upsert_documents(
            documents=documents,
            embeddings=embeddings
        )