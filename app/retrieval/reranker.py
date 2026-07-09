from transformers import AutoModelForSequenceClassification
from transformers import AutoTokenizer

import torch


class CrossEncoderReranker:

    def __init__(self):

        self.model_name = "BAAI/bge-reranker-base"

        self.tokenizer = AutoTokenizer.from_pretrained(
            self.model_name
        )

        self.model = AutoModelForSequenceClassification.from_pretrained(
            self.model_name
        )

        self.model.eval()

    def rerank(
        self,
        query,
        documents,
        top_k=5,
    ):

        scored_documents = []

        for document in documents:

            inputs = self.tokenizer(
                query,
                document.page_content,
                return_tensors="pt",
                truncation=True,
                max_length=512,
            )

            with torch.no_grad():

                score = (
                    self.model(**inputs)
                    .logits.squeeze()
                    .item()
                )

            scored_documents.append(
                (
                    score,
                    document,
                )
            )

        scored_documents.sort(
            key=lambda x: x[0],
            reverse=True,
        )

        return [
            doc
            for score, doc in scored_documents[:top_k]
        ]
