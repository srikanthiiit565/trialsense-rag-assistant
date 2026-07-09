"""Utilities for splitting documents into chunks."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.processing.metadata import create_chunk_metadata


class DocumentChunker:
    def __init__(self):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=600,
            chunk_overlap=100,
            separators=["\n\n", "\n", ". ", " ", ""],
        )

    def chunk_documents(self, documents: list[Document]):
        chunked_documents = []

        for document in documents:
            chunks = self.splitter.split_text(document.page_content)

            for index, chunk in enumerate(chunks):
                metadata = create_chunk_metadata(document, index)

                chunked_documents.append(
                    Document(
                        page_content=chunk,
                        metadata=metadata,
                    )
                )

        return chunked_documents


def chunk_documents(documents: List[Dict[str, Any]], chunk_size: int = 800, chunk_overlap: int = 120) -> List[Dict[str, Any]]:
    """Split a list of document dictionaries into smaller chunks."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", " ", ""],
    )

    chunks: List[Dict[str, Any]] = []
    for document in documents:
        text = document.get("summary") or document.get("content") or ""
        if not text:
            continue
        for index, chunk_text in enumerate(splitter.split_text(text), start=1):
            chunk = dict(document)
            chunk["chunk_text"] = chunk_text
            chunk["chunk_index"] = index
            chunks.append(chunk)

    return chunks


def save_chunks(chunks: List[Dict[str, Any]], output_path: str | Path = "data/chunks/chunks.json") -> None:
    """Persist chunks to disk as JSON."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(chunks, indent=2), encoding="utf-8")
