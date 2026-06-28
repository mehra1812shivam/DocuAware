from fastembed.rerank.cross_encoder import TextCrossEncoder


class RerankerService:

    def __init__(self):

        self.model = TextCrossEncoder(
            model_name="BAAI/bge-reranker-base"
        )

    def rerank(
        self,
        query: str,
        chunks: list
    ):

        documents = [
            chunk.payload["content"]
            for chunk in chunks
        ]

        scores = list(
            self.model.rerank(
                query,
                documents
            )
        )

        ranked = sorted(
            zip(chunks, scores),
            key=lambda x: x[1],
            reverse=True
        )

        return [chunk for chunk, _ in ranked]