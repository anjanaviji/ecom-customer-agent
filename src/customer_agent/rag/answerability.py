from langchain_groq import ChatGroq
from customer_agent.config import settings
from customer_agent.rag.retriever import get_retriever


llm = ChatGroq(
    groq_api_key=settings.groq_api_key,
    model="openai/gpt-oss-120b",
    temperature=0,
    max_tokens=100,
    reasoning_effort="low",
)


def check_answerability(query: str, documents: list) -> bool:

    context = "\n\n".join(
        document.page_content
        for document in documents
    )

    prompt = f"""
    You are checking whether a knowledge base contains enough information
    to answer a customer's question.

    Question:
    {query}

    Knowledge base context:
    {context}
    Can the context directly and sufficiently answer the question?
    Answer ONLY:
    YES
    or
    NO
    """

    response = llm.invoke(prompt)

    result = response.text.strip().upper()

    return result == "YES"

