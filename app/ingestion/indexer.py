from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings
from app.config.settings import settings

def create_vector_store(chunks):
    embeddings = OllamaEmbeddings(
        model=settings.embedding_model,
        base_url=settings.ollama_base_url,
    )

    vector_store = FAISS.from_documents(
        documents=chunks,
        embedding=embeddings, 
    )

    vector_store.save_local(settings.faiss_index_path)
    return vector_store