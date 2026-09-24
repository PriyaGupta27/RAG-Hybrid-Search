from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router

app = FastAPI(
    title="Hybrid RAG API",
    description=(
        "RAG pipeline using FAISS, BM25, "
        "RRF, reranking and Ollama."
    ),
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.get("/", tags=["Health"])
def health_check():
    return {
        "status": "healthy",
        "service": "Hybrid RAG API"
    }