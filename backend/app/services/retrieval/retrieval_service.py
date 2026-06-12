from app.services.embeddings.embedding_service import EmbeddingService
from app.services.vector_stores.qdrant_service import QdrantService


class RetrievalService:

    def __init__(self):

        self.embedding_service = EmbeddingService()
        self.qdrant_service = QdrantService()

    def retrieve(
        self,
        query: str,
        limit: int = 5
    ):

        query_embedding = self.embedding_service.embed(
            [query]
        )[0]

        results = self.qdrant_service.search(
            query_embedding=query_embedding,
            limit=limit
        )

        return results