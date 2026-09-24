from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Ollama
    ollama_base_url: str = "http://localhost:11434"
    llm_model: str = "llama3.2:latest"
    embedding_model: str = "nomic-embed-text:latest"

    # FAISS
    faiss_index_path: str = "./faiss_index"
    chunks_path: str = "./data/processed/chunks.pkl"

    # Retrieval
    vector_top_k: int = 10
    keyword_top_k: int = 10
    final_top_k: int = 5

    # Chunking
    chunk_size: int = 500
    chunk_overlap: int = 50

    # Reranking
    reranker_model: str = ("cross-encoder/ms-marco-MiniLM-L-6-v2")

    class Config:
        env_file = ".env"

settings = Settings()