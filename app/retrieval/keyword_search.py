from rank_bm25 import BM25Okapi
from app.config.settings import settings

class KeywordRetriever:
    def __init__(self, documents):
        self.documents = documents

        tokenized_documents = [
            document.page_content.lower().split()
            for document in documents
        ]

        self.bm25 = BM25Okapi(tokenized_documents)

    def search(self, query: str, k: int = 10):
        query_tokens = query.lower().split()

        scores = self.bm25.get_scores(query_tokens)

        ranked_indices = sorted(
            range(len(scores)),
            key=lambda i: scores[i],
            reverse=True
        )

        results = []

        for index in ranked_indices[:k]:
            document = self.documents[index]
            document.metadata["bm25_score"] = float(scores[index])
            results.append(document)

        return results