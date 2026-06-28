from pydantic import BaseModel

class Source(BaseModel):
    filename: str
    chunk_index: int

class ChatRequest(BaseModel):
    question: str

class ChatResponse(BaseModel):
    answer: str
    sources: list[Source]