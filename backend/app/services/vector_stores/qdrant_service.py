# app/services/vector_stores/qdrant_service.py

from qdrant_client import QdrantClient

from app.core.config import settings

from app.core.enums import SearchScope

from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct
)

from uuid import uuid4

from langchain_core.documents import Document

from qdrant_client.models import (
    Filter,
    FieldCondition,
    MatchValue
)


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
    
    def create_payload_indexes(self):
        self.client.create_payload_index(
            collection_name=settings.qdrant_collection,
            field_name="owner_id",
            field_schema="keyword"
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
    def search(self,query_embedding: list[float],owner_id: str,scope: SearchScope,limit: int = 5):
        if scope == SearchScope.MY_DOCUMENTS:
            query_filter = Filter(
                must=[
                    FieldCondition(
                        key="owner_id",
                        match=MatchValue(
                            value=owner_id
                        )
                    )
                ]
            )

        else:

            # TODO:
            # Implement ALL_ACCESSIBLE filter
            query_filter = Filter(
                must=[
                    FieldCondition(
                        key="owner_id",
                        match=MatchValue(
                            value=owner_id
                        )
                    )
                ]
            )


        return self.client.query_points(
            collection_name=settings.qdrant_collection,
            query=query_embedding,
            query_filter=query_filter,
            limit=limit
        ).points