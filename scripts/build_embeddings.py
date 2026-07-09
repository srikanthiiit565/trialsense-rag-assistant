"""Embedding build script entrypoint."""
import json

from langchain_core.documents import Document

from app.embeddings.vector_store import (
    VectorStore,
)

INPUT_FILE = "data/chunks/chunks.json"


def load_chunks():

    with open(
        INPUT_FILE,
        "r",
        encoding="utf-8",
    ) as f:

        data = json.load(f)

    documents = []

    for item in data:

        documents.append(

            Document(
                page_content=item["page_content"],
                metadata=item["metadata"],
            )

        )

    return documents


def main():

    print("=" * 60)
    print("Loading Chunks")
    print("=" * 60)

    documents = load_chunks()

    print(f"Loaded {len(documents)} chunks")

    print("=" * 60)
    print("Creating ChromaDB")
    print("=" * 60)

    vector_store = VectorStore()

    vector_store.add_documents(
        documents
    )

    print("=" * 60)
    print("Embedding Complete")
    print("=" * 60)


if __name__ == "__main__":
    main()