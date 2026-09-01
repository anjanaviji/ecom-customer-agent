from collections import defaultdict

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


def split_documents(documents: list[Document]) -> list[Document]:

    splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", " ", ""],
        chunk_size=500,
        chunk_overlap=50)
    
    counters = defaultdict(int)

    chunks = splitter.split_documents(documents)
    for chunk in chunks:
        source = chunk.metadata["source"]

        document_name = source.rsplit(".", 1)[0]

        chunk.metadata["chunk_id"] = (
            f"{document_name}_{counters[source]}"
        )

        counters[source] += 1
    return chunks