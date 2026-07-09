"""Embedding model wrapper."""
from langchain_community.embeddings import HuggingFaceEmbeddings


class EmbeddingModel:
    def __init__(self):
        self.model = HuggingFaceEmbeddings(
            model_name="BAAI/bge-base-en-v1.5",
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": True},
        )

    def get_model(self):
        return self.model

    def embed_documents(self, documents):
        return self.model.embed_documents(documents)

    def embed_query(self, query):
        return self.model.embed_query(query)