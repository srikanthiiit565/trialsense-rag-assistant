import json
import os

from langchain_core.documents import Document

from app.processing.chunker import (
    DocumentChunker,
)


INPUT_FILE = "data/processed/documents.json"

OUTPUT_DIR = "data/chunks"


def load_documents():

    with open(
        INPUT_FILE,
        "r",
        encoding="utf-8",
    ) as f:

        raw_docs = json.load(f)

    documents = []

    for item in raw_docs:

        text = item.get("summary", "")

        if not text:
            continue

        metadata = dict(item)

        metadata.pop("summary", None)

        documents.append(

            Document(
                page_content=text,
                metadata=metadata,
            )

        )

    return documents


def save_chunks(chunks):

    os.makedirs(
        OUTPUT_DIR,
        exist_ok=True,
    )

    data = []

    for chunk in chunks:

        data.append(

            {

                "page_content": chunk.page_content,

                "metadata": chunk.metadata,

            }

        )

    with open(
        f"{OUTPUT_DIR}/chunks.json",
        "w",
        encoding="utf-8",
    ) as f:

        json.dump(
            data,
            f,
            indent=4,
        )


def main():

    documents = load_documents()

    print(f"Loaded {len(documents)} documents")

    chunker = DocumentChunker()

    chunks = chunker.chunk_documents(
        documents
    )

    print(f"Generated {len(chunks)} chunks")

    save_chunks(chunks)

    print("Chunks saved successfully")


if __name__ == "__main__":
    main()
