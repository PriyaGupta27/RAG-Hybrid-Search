from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from app.pipeline.rag_pipeline import RAGPipeline
from app.schemas.models import QueryRequest, QueryResponse

router = APIRouter(
    prefix="/api/v1",
    tags=["RAG"]
)

rag_pipeline = RAGPipeline()

@router.post("/query", response_model=QueryResponse)
def query_rag(request: QueryRequest):
    try:
        return rag_pipeline.run(
            question=request.question,
            top_k=request.top_k
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"RAG pipeline failed: {str(e)}"
        )

@router.post("/query/stream")
def query_rag_stream(request: QueryRequest):
    try:
        return StreamingResponse(
            rag_pipeline.stream(
                question=request.question,
                top_k=request.top_k
            ),
            media_type="text/plain"
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"RAG streaming failed: {str(e)}"
        )