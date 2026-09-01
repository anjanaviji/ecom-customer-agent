from langchain.tools import tool

from customer_agent.rag.retriever import get_retriever
from customer_agent.rag.reranker import Reranker


retriever = get_retriever(k=20)
reranker = Reranker()



@tool
def search_knowledge(query: str) -> str:
    """Search customer support policies and knowledge base.

    Use this tool when the customer asks about policies,
    returns, refunds, shipping, cancellations, or other
    company knowledge.
    """

    documents = retriever.invoke(query)

    if not documents:
        return "No relevant information found."
    
    reranked = reranker.rerank(
        query,
        documents,
        top_k=5,
        )
    documents = [
        document
        for document, score in reranked
    ]

    return "\n\n".join(
        f"Source: {doc.metadata.get('source', 'unknown')}\n"
        f"{doc.page_content}"
        for doc in documents
    )
