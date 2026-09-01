from customer_agent.rag.retriever import get_retriever
from customer_agent.rag.reranker import Reranker


retriever = get_retriever(k=20)
reranker = Reranker()

query = "When can I expect the refund?"

documents = retriever.invoke(query)

print("\nVECTOR SEARCH")
print("==============================")

for rank, document in enumerate(documents, start=1):
    print(
        rank,
        document.metadata["chunk_id"],
    )


reranked = reranker.rerank(
    query,
    documents,
    top_k=5,
)

print("\nRERANKED")
print("==============================")

# for rank, (document, score) in enumerate(
#     reranked,
#     start=1,
# ):
#     print(
#         rank,
#         document.metadata["chunk_id"],
#         round(float(score), 4),
#     )
for doc, score in reranked:
    print("=" * 70)
    print("SCORE:", score)
    print("CHUNK:", doc.metadata.get("chunk_id"))
    print(doc.page_content[:500])