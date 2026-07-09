from __future__ import annotations

from dataclasses import dataclass
from typing import Any
import time

from langchain_ollama import ChatOllama

from app.retrieval.hybrid_retriever import HybridRetriever
from app.retrieval.reranker import CrossEncoderReranker

from app.utils.config import settings
from app.agents.prompts import SYSTEM_PROMPT

from app.guardrails.guardrail_manager import check_output

from app.analytics.logger import log_query
from langchain_ollama import ChatOllama

from app.utils.config import settings
from app.agents.prompts import SYSTEM_PROMPT

from app.guardrails.guardrail_manager import check_output

from app.analytics.logger import log_query


import time
start_time = time.time()

@dataclass
class Node:
    """Represents a node in the agent decision graph."""
    id: str
    type: str
    data: Any = None


retriever = HybridRetriever()
reranker = CrossEncoderReranker()
from app.guardrails.guardrail_manager import (
    check_input,
    check_output
)

def retrieve_node(state):

    def _get(s, k, default=None):
        try:
            return s[k]
        except Exception:
            return getattr(s, k, default)

    def _set(s, k, v):
        try:
            s[k] = v
        except Exception:
            setattr(s, k, v)

    query = _get(state, "query")

    docs = retriever.retrieve(query, vector_k=5, bm25_k=5)

    _set(state, "retrieved_documents", docs)

    return state



def retrieve_node(state):

    def _get(s, k, default=None):
        try:
            return s[k]
        except Exception:
            return getattr(s, k, default)

    def _set(s, k, v):
        try:
            s[k] = v
        except Exception:
            setattr(s, k, v)


    # -----------------------------
    # Get user query
    # -----------------------------

    query = _get(state, "query")


    # -----------------------------
    # Input Guardrail
    # -----------------------------

    from app.guardrails.guardrail_manager import check_input


    guard_result = check_input(query)


    # If query is unsafe
    if not guard_result["allowed"]:

        _set(
            state,
            "guardrail_blocked",
            True
        )

        _set(
            state,
            "answer",
            guard_result["message"]
        )

        return state


    # Use cleaned query
    query = guard_result["query"]


    _set(
        state,
        "query",
        query
    )


    # -----------------------------
    # Retrieval
    # -----------------------------

    docs = retriever.retrieve(
        query,
        vector_k=5,
        bm25_k=5
    )


    # -----------------------------
    # Retrieval Guardrail
    # -----------------------------

    from app.guardrails.guardrail_manager import (
        check_retrieval
    )


    context_valid = check_retrieval(
        docs
    )


    if not context_valid:

        _set(
            state,
            "guardrail_blocked",
            True
        )

        _set(
            state,
            "answer",
            (
                "I could not find enough "
                "reliable clinical evidence "
                "to answer this question."
            )
        )

        return state


    # -----------------------------
    # Save Documents
    # -----------------------------

    _set(
        state,
        "retrieved_documents",
        docs
    )


    _set(
        state,
        "guardrail_blocked",
        False
    )


    return state



def build_context_node(state):

    def _get(s, k, default=None):
        try:
            return s[k]
        except Exception:
            return getattr(s, k, default)

    def _set(s, k, v):
        try:
            s[k] = v
        except Exception:
            setattr(s, k, v)

    reranked = _get(state, "reranked_documents", []) or []

    context = "\n\n".join([doc.page_content for doc in reranked])

    citations = [doc.metadata.get("document_id", "unknown") for doc in reranked]

    _set(state, "context", context)
    _set(state, "citations", citations)

    return state


# Node 4: generate answers
import logging
from app.utils.config import settings
from app.agents.prompts import SYSTEM_PROMPT
from app.agents.groq_client import GroqClient
from app.agents.groq_http import GroqHTTPClient
from langchain_ollama import ChatOllama

logger = logging.getLogger(__name__)


def _get_llm():
    """Lazily return an LLM instance. Prefer Groq when configured, else Ollama.

    Raises a RuntimeError with a helpful message if no client is available.
    """
    if settings.GROQ_API_KEY:
        # Prefer raw HTTP client for Groq if possible (more predictable)
        try:
            return GroqHTTPClient(api_key=settings.GROQ_API_KEY, model=settings.GROQ_MODEL or "llama3.1", base_url=settings.GROQ_BASE_URL)
        except Exception:
            try:
                return GroqClient(api_key=settings.GROQ_API_KEY, model=settings.GROQ_MODEL or "llama3.1", base_url=settings.GROQ_BASE_URL)
            except Exception:
                pass

    if settings.OLLAMA_BASE_URL and settings.OLLAMA_MODEL:
        return ChatOllama(model=settings.OLLAMA_MODEL, base_url=settings.OLLAMA_BASE_URL, temperature=0)

    raise RuntimeError("No configured LLM client: set GROQ_API_KEY or OLLAMA_BASE_URL/OLLAMA_MODEL in environment")


import time

from langchain_ollama import ChatOllama

from app.utils.config import settings
from app.agents.prompts import SYSTEM_PROMPT

from app.guardrails.guardrail_manager import check_output

from app.analytics.logger import log_query



# Initialize LLM once
llm = ChatOllama(
    model=settings.OLLAMA_MODEL,
    base_url=settings.OLLAMA_BASE_URL,
    temperature=0
)

def rerank_node(state):

    def _get(s, k, default=None):
        try:
            return s[k]
        except Exception:
            return getattr(s, k, default)

    def _set(s, k, v):
        try:
            s[k] = v
        except Exception:
            setattr(s, k, v)


    query = _get(
        state,
        "query"
    )


    docs = _get(
        state,
        "retrieved_documents",
        []
    )


    reranked_docs = reranker.rerank(
        query,
        docs,
        top_k=5
    )


    _set(
        state,
        "reranked_documents",
        reranked_docs
    )


    return state

import time

from langchain_ollama import ChatOllama

from app.utils.config import settings
from app.agents.prompts import SYSTEM_PROMPT

from app.guardrails.guardrail_manager import check_output
from app.analytics.logger import log_query



llm = ChatOllama(
    model=settings.OLLAMA_MODEL,
    base_url=settings.OLLAMA_BASE_URL,
    temperature=0
)



def answer_node(state):

    start_time = time.time()


    # -----------------------------
    # State helpers
    # -----------------------------

    def _get(s, k, default=None):
        try:
            return s[k]
        except Exception:
            return getattr(s, k, default)


    def _set(s, k, v):
        try:
            s[k] = v
        except Exception:
            setattr(s, k, v)



    # -----------------------------
    # Read State
    # -----------------------------

    query = _get(
        state,
        "query",
        ""
    )


    context = _get(
        state,
        "context",
        ""
    )


    citations = _get(
        state,
        "citations",
        []
    )



    # -----------------------------
    # Build Prompt
    # -----------------------------

    prompt = f"""

{SYSTEM_PROMPT}


Clinical Evidence:

-------------------

{context}

-------------------


Question:

{query}


Rules:

- Answer only using the evidence.
- Do not hallucinate.
- If evidence is insufficient, say so.
- Mention relevant study IDs.

"""



    # -----------------------------
    # Generate Answer
    # -----------------------------

    try:

        response = llm.invoke(
            prompt
        )

        answer = response.content

        success = True


    except Exception as e:

        answer = (
            f"LLM generation failed: {str(e)}"
        )

        success = False



    # -----------------------------
    # Output Guardrail
    # -----------------------------

    answer = check_output(
        answer
    )



    # -----------------------------
    # Save Answer
    # -----------------------------

    _set(
        state,
        "answer",
        answer
    )



    # -----------------------------
    # Analytics
    # -----------------------------

    latency = round(
        time.time() - start_time,
        2
    )


    log_query(

        query=query,

        answer=answer,

        citations=citations,

        latency=latency,

        model=settings.OLLAMA_MODEL,

        success=success

    )


    return state