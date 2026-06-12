# app/services/vector_stores/qdrant_service.py

from qdrant_client import QdrantClient

from app.core.config import settings

from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct
)

from uuid import uuid4

from langchain_core.documents import Document


class QdrantService:

    def __init__(self):

        self.client = QdrantClient(
            url=settings.qdrant_url,
            api_key=settings.qdrant_api_key
        )

    def create_collection(self):

        collections = self.client.get_collections()

        existing = [
            collection.name
            for collection in collections.collections
        ]

        if settings.qdrant_collection in existing:
            return

        self.client.create_collection(
            collection_name=settings.qdrant_collection,
            vectors_config=VectorParams(
                size=384,
                distance=Distance.COSINE
            )
        )
    def upsert_documents(
            self,
            documents: list[Document],
            embeddings: list[list[float]]
        ):

        points = []

        for document, embedding in zip(
            documents,
            embeddings
        ):

            points.append(
                PointStruct(
                    id=str(uuid4()),
                    vector=embedding,
                    payload={
                        **document.metadata,
                        "content": document.page_content
                    }
                )
            )

        self.client.upsert(
            collection_name=settings.qdrant_collection,
            points=points
        )
    def search(self,query_embedding: list[float],limit: int = 5):

        return self.client.query_points(
            collection_name=settings.qdrant_collection,
            query=query_embedding,
            limit=limit
        ).points