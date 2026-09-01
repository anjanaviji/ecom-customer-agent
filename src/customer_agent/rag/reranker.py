from sentence_transformers import CrossEncoder


class Reranker:

    def __init__(self,model_name: str = "BAAI/bge-reranker-base"):
        self.model = CrossEncoder(model_name)

    def rerank(self,query: str,documents: list,top_k: int = 5):
        pairs = [(query, document.page_content)for document in documents]

        scores = self.model.predict(pairs)

        ranked = sorted(
            zip(documents, scores),
            key=lambda x: x[1],
            reverse=True,
        )

        return ranked[:top_k]