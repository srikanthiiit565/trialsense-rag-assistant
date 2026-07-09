"""RAG agent implementation."""

from app.agents.graph import rag_graph


class RAGAgent:

	def ask(

		self,

		query: str,

	):

		state = {

			"query": query,

			"retrieved_documents": [],

			"reranked_documents": [],

			"context": "",

			"answer": "",

			"citations": [],

		}

		return rag_graph.invoke(state)
