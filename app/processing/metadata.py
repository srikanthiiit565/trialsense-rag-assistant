"""Helpers for attaching metadata to processed documents."""
from __future__ import annotations

from typing import Any, Dict, List
from uuid import uuid4


def add_metadata(documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Attach a simple metadata block to each document."""
    for document in documents:
        document.setdefault("metadata", {})
        document["metadata"].setdefault("source", document.get("source", "unknown"))
        document["metadata"].setdefault("document_id", document.get("id", ""))
    return documents


def create_chunk_metadata(document: Any, chunk_index: int) -> Dict[str, Any]:
    """Standardize metadata for every chunk."""
    if hasattr(document, "metadata"):
        metadata = dict(getattr(document, "metadata", {}) or {})
    elif isinstance(document, dict):
        metadata = dict(document.get("metadata", {}))
    else:
        metadata = {}

    metadata["chunk_id"] = str(uuid4())
    metadata["chunk_index"] = chunk_index
    metadata["document_id"] = metadata.get("document_id") or metadata.get("id") or "unknown"
    return metadata
