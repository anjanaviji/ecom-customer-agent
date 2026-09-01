from pathlib import Path
from webbrowser import get

from langchain_chroma import Chroma
from langchain_core.documents import Document

from customer_agent.rag.embeddings import get_embedding_model


CHROMA_DIR = Path("data/chroma")


def create_vectorstore(documents: list[Document]) -> Chroma:

    embeddings = get_embedding_model()

    return Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=str(CHROMA_DIR),
        collection_name="customer_knowledge",
    )