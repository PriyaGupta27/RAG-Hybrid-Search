from collections import defaultdict

class HybridRetriever:
    def __init__(self,vector_retriever,keyword_retriever,rrf_k: int = 60):
        self.vector_retriever = vector_retriever
        self.keyword_retriever = keyword_retriever
        self.rrf_k = rrf_k

    def search(self, query: str):
        vector_results = (self.vector_retriever.search(query))
        keyword_results = (self.keyword_retriever.search(query))
        scores = defaultdict(float)
        documents = {}

        # Vector ranking
        for rank, document in enumerate(vector_results, start=1):
            chunk_id = document.metadata.get("chunk_id")
            if chunk_id is None:
                continue
            scores[chunk_id] += (1 / (self.rrf_k + rank))
            documents[chunk_id] = document

        # Keyword ranking
        for rank, document in enumerate(keyword_results,start=1):
            chunk_id = document.metadata.get("chunk_id")
            if chunk_id is None:
                continue
            scores[chunk_id] += (1 / (self.rrf_k + rank))
            documents[chunk_id] = document

        ranked = sorted(
            scores.items(),
            key=lambda x: x[1],
            reverse=True
        )

        results = []

        for chunk_id, score in ranked:
            document = documents[chunk_id]
            document.metadata["rrf_score"] = score
            results.append(document)

        return results