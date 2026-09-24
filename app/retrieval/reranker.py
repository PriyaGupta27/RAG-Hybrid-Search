from sentence_transformers import CrossEncoder
from app.config.settings import settings

class Reranker:
    def __init__(self):
        self.model = CrossEncoder(settings.reranker_model)

    def rerank(self,query: str,documents,top_k: int = 5):
        pairs = [(
                query,
                document.page_content
            ) for document in documents
        ]

        scores = self.model.predict(pairs)
        scored_documents = list(zip(documents, scores))
        scored_documents.sort(key=lambda x: x[1], reverse=True)
        results = []

        for document, score in scored_documents[:top_k]:
            document.metadata["reranker_score"] = float(score)
            results.append(document)

        return results