"""Vector store integration."""
from langchain_chroma import Chroma

from app.embeddings.embedding_model import EmbeddingModel
from app.utils.config import settings


class VectorStore:
    def __init__(self, embedding_model=None, persist_directory=None):
        if embedding_model is None:
            embedding_model = EmbeddingModel()
        if persist_directory is None:
            persist_directory = settings.CHROMA_DB_PATH

        self.db = Chroma(
            persist_directory=persist_directory,
            embedding_function=embedding_model.get_model(),
            collection_name="clinical_trials",
        )

    def add_documents(self, documents):
        self.db.add_documents(documents)

    def similarity_search(self, query, k=5):
        return self.db.similarity_search(query, k=k)

    def similarity_search_with_score(self, query, k=5):
        return self.db.similarity_search_with_score(query, k=k)