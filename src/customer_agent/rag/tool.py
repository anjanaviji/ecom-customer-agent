from langchain.tools import tool

from customer_agent.rag.retriever import get_retriever
from customer_agent.rag.reranker import Reranker
from customer_agent.rag.answerability import check_answerability


retriever = get_retriever(k=20)
reranker = Reranker()



@tool
def search_knowledge(query: str) -> str:
    """Search customer support policies and knowledge base.

    Use this tool when the customer asks about policies,
    returns, refunds, shipping, cancellations, or other
    company knowledge.
    """

    # 1. Retrieve
    documents = retriever.invoke(query)

    if not documents:
        return "No relevant information found."
    #Rerank
    reranked = reranker.rerank(
        query,
        documents,
        top_k=5,
        )
    documents = [
        document
        for document, score in reranked
    ]

    # 3. Check answerability
    answerable = check_answerability(query,documents)

    if not answerable:
        return "No sufficient information found in the knowledge base."

    return "\n\n".join(
        f"Source: {doc.metadata.get('source', 'unknown')}\n"
        f"{doc.page_content}"
        for doc in documents
    )
