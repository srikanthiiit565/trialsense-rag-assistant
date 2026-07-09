import json

from langchain_core.documents import Document
from rank_bm25 import BM25Okapi


class BM25Retriever:

    def __init__(
        self,
        chunk_file="data/chunks/chunks.json",
    ):

        with open(
            chunk_file,
            "r",
            encoding="utf-8",
        ) as f:

            data = json.load(f)

        self.documents = []

        corpus = []

        for item in data:

            document = Document(
                page_content=item["page_content"],
                metadata=item["metadata"],
            )

            self.documents.append(document)

            corpus.append(
                item["page_content"].lower().split()
            )

        self.bm25 = BM25Okapi(corpus)

    def search(
        self,
        query,
        k=5,
    ):

        tokens = query.lower().split()

        scores = self.bm25.get_scores(tokens)

        ranked = sorted(
            zip(scores, self.documents),
            reverse=True,
            key=lambda x: x[0],
        )

        return [
            doc
            for score, doc in ranked[:k]
        ]
