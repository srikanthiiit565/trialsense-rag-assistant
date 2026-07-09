from app.retrieval.hybrid_retriever import (
    HybridRetriever,
)


def main():

    retriever = HybridRetriever()

    query = (
        "latest Alzheimer's monoclonal antibody treatment"
    )

    documents = retriever.retrieve(
        query,
        vector_k=5,
        bm25_k=5,
    )

    print("=" * 80)

    print(
        f"Retrieved {len(documents)} documents"
    )

    print("=" * 80)

    for i, doc in enumerate(documents, start=1):

        print(f"\nDocument {i}")

        print("-" * 40)

        print(doc.page_content[:300])

        print()

        print(doc.metadata)


if __name__ == "__main__":
    main()
