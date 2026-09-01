from langchain_chroma import Chroma

from customer_agent.rag.embeddings import get_embedding_model
from customer_agent.rag.vector_store import CHROMA_DIR


def get_retriever(k: int = 5):

    embeddings = get_embedding_model()

    vectorstore = Chroma(
        collection_name="customer_knowledge",
        persist_directory=str(CHROMA_DIR),
        embedding_function=embeddings,
    )

    return vectorstore.as_retriever(
        search_kwargs={
            "k": k,
        }
    )