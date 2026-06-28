from app.services.retrieval.retrieval_service import RetrievalService
from app.services.reranking.reranker_service import RerankerService
from app.services.prompting.prompt_builder import PromptBuilder
from app.services.llm.gemini_service import GeminiService
from app.core.enums import SearchScope
import time 

class ChatService:

    def __init__(self):

        self.retrieval_service = RetrievalService()
        self.reranker_service = RerankerService()
        self.prompt_builder = PromptBuilder()
        self.gemini_service = GeminiService()

    def chat(
        self,
        question: str,
        owner_id: str,
        department: str,
        scope: SearchScope
    ) -> str:
        start = time.perf_counter()
        chunks = self.retrieval_service.retrieve(
            query=question,
            owner_id=owner_id,
            department=department,
            scope=scope,
            limit=10
        )
        print(f"Retrieve: {time.perf_counter()-start:.2f}s")

        t = time.perf_counter()

        ranked_chunks = self.reranker_service.rerank(
            query=question,
            chunks=chunks
        )
        print(f"Rerank: {time.perf_counter()-t:.2f}s")

        top_chunks = ranked_chunks[:5]

        t = time.perf_counter()
        prompt = self.prompt_builder.build(
            question=question,
            chunks=top_chunks
        )
        print(f"Prompt: {time.perf_counter()-t:.2f}s")

        t = time.perf_counter()

        answer = self.gemini_service.generate(prompt)
        print(f"Gemini: {time.perf_counter()-t:.2f}s")

        print(f"Total: {time.perf_counter()-start:.2f}s")

        sources = [
            {
                "filename": chunk.payload["filename"],
                "chunk_index": chunk.payload["chunk_index"]
            }
            for chunk in top_chunks
        ]

        return {
            "answer": answer,
            "sources": sources
        }