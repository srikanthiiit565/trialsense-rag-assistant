from app.embeddings.vector_store import (
    VectorStore,
)

from app.retrieval.bm25_retriever import (
    BM25Retriever,
)


class HybridRetriever:

    def __init__(self):

        self.vector_store = VectorStore()

        self.bm25 = BM25Retriever()

    def retrieve(
        self,
        query,
        vector_k=5,
        bm25_k=5,
    ):

        vector_docs = self.vector_store.similarity_search(
            query,
            k=vector_k,
        )

        keyword_docs = self.bm25.search(
            query,
            k=bm25_k,
        )

        merged = {}

        for doc in vector_docs:

            merged[
                doc.metadata["chunk_id"]
            ] = doc

        for doc in keyword_docs:

            merged[
                doc.metadata["chunk_id"]
            ] = doc

        return list(merged.values())
