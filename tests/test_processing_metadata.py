from langchain_core.documents import Document

from app.processing.metadata import create_chunk_metadata


def test_create_chunk_metadata_accepts_langchain_document():
    document = Document(
        page_content="Example text",
        metadata={"source": "pubmed", "document_id": "123"},
    )

    metadata = create_chunk_metadata(document, 2)

    assert metadata["source"] == "pubmed"
    assert metadata["document_id"] == "123"
    assert metadata["chunk_index"] == 2
    assert "chunk_id" in metadata
