from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional, TypedDict

from langchain_core.documents import Document


@dataclass
class AgentState:
    """State container used by the agent graph.

    This dataclass exposes the fields expected by nodes so the graph can
    instantiate a concrete object and nodes can access attributes directly.
    """
    query: Optional[str] = ""
    retrieved_documents: List[Document] = field(default_factory=list)
    reranked_documents: List[Document] = field(default_factory=list)
    context: str = ""
    answer: str = ""
    citations: List[str] = field(default_factory=list)
    conversation_history: List[str] = field(default_factory=list)
    last_action: Optional[str] = None
    context_meta: dict = field(default_factory=dict)


class AgentStateDict(TypedDict):
    """TypedDict representation of agent state for static typing."""

    query: str
    retrieved_documents: list[Document]
    reranked_documents: list[Document]
    context: str
    answer: str
    citations: list[str]
