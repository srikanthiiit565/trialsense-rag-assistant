from app.retrieval.hybrid_retriever import (
    HybridRetriever,
)

from app.retrieval.reranker import (
    CrossEncoderReranker,
)


def main():

    query = (
        "latest Alzheimer's monoclonal antibody treatment"
    )

    retriever = HybridRetriever()

    candidates = retriever.retrieve(
        query,
        vector_k=5,
        bm25_k=5,
    )

    print(
        f"Retrieved {len(candidates)} candidate documents"
    )

    reranker = CrossEncoderReranker()

    final_docs = reranker.rerank(
        query,
        candidates,
        top_k=5,
    )

    print()

    print("=" * 80)

    print("Top Ranked Documents")

    print("=" * 80)

    for i, doc in enumerate(final_docs, start=1):

        print(f"\nRank {i}")

        print("-" * 40)

        print(doc.page_content[:300])

        print()

        print(doc.metadata)


if __name__ == "__main__":
    main()
