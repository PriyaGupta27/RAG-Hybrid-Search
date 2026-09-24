from app.retrieval.vector_search import VectorRetriever
from app.retrieval.keyword_search import KeywordRetriever
from app.retrieval.hybrid_search import HybridRetriever
from app.retrieval.reranker import Reranker
from app.generation.llm import LLM
from app.generation.prompt import SYSTEM_PROMPT
from app.config.settings import settings

class RAGPipeline:
    def __init__(self):
        print("\nInitializing RAG Pipeline...")

        # Load chunks
        print("Loading chunks...")
        chunks = self._load_chunks()
        print(f"Loaded {len(chunks)} chunks.")

        # Initialise FAISS retriever
        print("Loading FAISS retriever...")
        self.vector_retriever = ( VectorRetriever())

        # Initialise BM25 retriever
        print("Building BM25 retriever...")
        self.keyword_retriever = ( KeywordRetriever(chunks))

        # Initialise Hybrid retriever
        print("Initializing hybrid retriever...")
        self.hybrid_retriever = (
            HybridRetriever(
                vector_retriever=self.vector_retriever,
                keyword_retriever=self.keyword_retriever
            )
        )

        # Initialise reranker
        print("Loading reranker...")
        self.reranker = Reranker()

        # Initialise LLM
        print("Loading LLM...")
        self.llm = LLM()
        print("RAG Pipeline initialized successfully.")

    # Load Persisted chunks
    def _load_chunks(self):
        import pickle
        from pathlib import Path

        chunks_path = Path( settings.chunks_path)

        if not chunks_path.exists():
            raise FileNotFoundError(
                f"Chunks file not found: "
                f"{chunks_path}\n\n"
                f"Run ingestion first:\n"
                f"python ingest.py"
            )

        with open(chunks_path, "rb") as file:
            chunks = pickle.load(file)
        return chunks

    #--------------------RUN-------------------------
    def run(self, question: str, top_k: int = 5):
        if not question or not question.strip():
            return {
                "answer": (
                    "Please provide a question."
                ),
                "sources": []
            }

        question = question.strip()

        print("\nRunning hybrid retrieval...")
        candidates = (
            self.hybrid_retriever.search(
                question
            )
        )

        if not candidates:
            return {
                "answer": (
                    "I could not find relevant "
                    "information in the documents."
                ),
                "sources": []
            }

        print(f"Retrieved {len(candidates)} candidates.")

        print("Reranking candidates...")
        ranked_documents = (
            self.reranker.rerank(
                query=question,
                documents=candidates,
                top_k=top_k
            )
        )

        if not ranked_documents:
            return {
                "answer": (
                    "I could not find sufficiently "
                    "relevant information."
                ),
                "sources": []
            }

        print(f"Selected {len(ranked_documents)} documents after reranking.")

        context_parts = []
        for index, document in enumerate(ranked_documents, start=1):
            source = document.metadata.get("source","unknown")
            page = document.metadata.get("page","unknown")
            chunk_id = document.metadata.get("chunk_id","unknown")
            content = document.page_content.strip()
            context_parts.append(
                f"""[Context {index}]
                    Source: {source}
                    Page: {page}
                    Chunk ID: {chunk_id}
                    {content}
                """
            )

        context = "\n".join(
            context_parts
        )

        prompt = SYSTEM_PROMPT.format(
            context=context,
            question=question
        )

        print("Generating answer with Ollama...")
        answer = self.llm.generate(prompt)

        sources = []
        for document in ranked_documents:
            sources.append(
                {
                    "source": document.metadata.get("source","unknown"),
                    "page": document.metadata.get("page","unknown"),
                    "chunk_id": document.metadata.get("chunk_id","unknown"),
                    "rrf_score": document.metadata.get("rrf_score"),
                    "reranker_score": document.metadata.get("reranker_score")
                }
            )

        return {
            "question": question,
            "answer": answer,
            "sources": sources
        }

    def stream(self, question: str, top_k: int = 5):
        if not question or not question.strip():
            yield "Please provide a question."
            return

        question = question.strip()

        print("\nRunning hybrid retrieval...")
        candidates = self.hybrid_retriever.search(question)

        if not candidates:
            yield "I could not find relevant information in the documents."
            return

        print(f"Retrieved {len(candidates)} candidates.")
        print("Reranking candidates...")
        ranked_documents = self.reranker.rerank(
            query=question,
            documents=candidates,
            top_k=top_k
        )

        if not ranked_documents:
            yield "I could not find sufficiently relevant information."
            return

        print(f"Selected {len(ranked_documents)} documents after reranking.")
        context_parts = []
        for index, document in enumerate( ranked_documents, start=1):
            source = document.metadata.get("source","unknown")
            page = document.metadata.get("page","unknown")
            chunk_id = document.metadata.get("chunk_id", "unknown")

            content = document.page_content.strip()
            context_parts.append(
                f"""[Context {index}]
                Source: {source}
                Page: {page}
                Chunk ID: {chunk_id}
                {content}
                """
            )

        context = "\n".join(context_parts)
        prompt = SYSTEM_PROMPT.format(context=context, question=question)

        print("Streaming answer from Ollama...")
        for token in self.llm.stream(prompt):
            yield token