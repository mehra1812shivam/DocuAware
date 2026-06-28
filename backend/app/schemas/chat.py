from pydantic import BaseModel
from app.core.enums import SearchScope

class Source(BaseModel):
    filename: str
    chunk_index: int

class ChatRequest(BaseModel):
    question: str
    scope: SearchScope = SearchScope.MY_DOCUMENTS

class ChatResponse(BaseModel):
    answer: str
    sources: list[Source]