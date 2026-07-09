"""Retrieval evaluation utilities."""
from app.retrieval.hybrid_retriever import (
    HybridRetriever
)



retriever = HybridRetriever()



def calculate_recall(

        retrieved_ids,

        expected_ids

):

    hits = 0


    for doc in expected_ids:

        if doc in retrieved_ids:

            hits += 1


    return hits / len(expected_ids)



def evaluate_retrieval(dataset):

    results = []


    for item in dataset:


        docs = retriever.retrieve(

            item["question"],

            vector_k=5,

            bm25_k=5

        )


        retrieved_ids = [

            doc.metadata.get(
                "document_id"
            )

            for doc in docs

        ]


        recall = calculate_recall(

            retrieved_ids,

            item["expected_sources"]

        )


        results.append(

            {

                "question":
                item["question"],


                "recall":
                recall

            }

        )


    return results