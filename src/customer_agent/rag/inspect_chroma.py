from langchain_chroma import Chroma

from customer_agent.rag.embeddings import get_embedding_model
from customer_agent.rag.vector_store import CHROMA_DIR


vectorstore = Chroma(
    collection_name="customer_knowledge",
    persist_directory=str(CHROMA_DIR),
    embedding_function=get_embedding_model(),
)

documents = vectorstore.similarity_search(
    "cancellation",
    k=20,
)

for i, document in enumerate(documents, start=1):
    chunk_id = document.metadata.get("chunk_id", "")

    if chunk_id.startswith("cancellation_policy"):
        print("=" * 80)
        print(f"CHUNK ID: {chunk_id}")
        print(f"SOURCE:   {document.metadata.get('source', 'unknown')}")
        print("-" * 80)
        print(document.page_content)
        print()