from customer_agent.rag.loader import load_documents
from customer_agent.rag.splitter import split_documents
from customer_agent.rag.vector_store import create_vectorstore
from customer_agent.config import settings


def ingest():
    print("Starting ingestion process...")

    documents = load_documents(settings.knowledge_base_path)

    print(f"Loaded documents: {len(documents)}")

    chunks = split_documents(documents)

    print(f"Created chunks: {len(chunks)}")

    create_vectorstore(chunks)

    print("Vector store created successfully.")


if __name__ == "__main__":
    ingest()