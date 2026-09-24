from pydantic import BaseModel, Field

class QueryRequest(BaseModel):
    question: str = Field(...,min_length=1, description="Question to ask RAG System")
    top_k: int = Field(default=5, ge=1, le=20, description="Number of final documents to return")

class Source(BaseModel):
    source: str
    page: int | str | None = None
    chunk_id: str | None = None
    score: float | None = None
    reranker_score: float | None = None

class QueryResponse(BaseModel):
    question: str
    answer: str
    sources: list[Source]