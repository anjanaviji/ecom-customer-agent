from pathlib import Path
from langchain_core.documents import Document

from customer_agent.config import settings


def load_documents(path: str) -> list[Document]:
    documents = []
    
    for file_path in Path(path).glob("*.md"):
        content = file_path.read_text(encoding="utf-8")

        documents.append(
            Document(
                page_content=content,
                metadata={
                    "source": file_path.name,
                },
            )
        )

    return documents