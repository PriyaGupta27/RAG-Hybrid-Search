from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from app.config.settings import settings

class VectorRetriever:
    def __init__(self):
        embeddings = OllamaEmbeddings(
            model=settings.embedding_model,
            base_url=settings.ollama_base_url,
        )

        self.vector_store = FAISS.load_local(
            folder_path=settings.faiss_index_path,
            embeddings=embeddings,
            allow_dangerous_deserialization=True
        )

        print("FAISS index loaded successfully")

    def search(self, query: str):
        return self.vector_store.similarity_search(
            query,
            k=settings.vector_top_k,
        )