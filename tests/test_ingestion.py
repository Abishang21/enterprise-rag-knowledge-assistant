from unittest.mock import patch

import pytest

from src.ingestion.chunker import chunk_text
from src.ingestion.document_parser import parse_document
from src.ingestion.embedder import Embedder


def test_chunk_text_creates_chunks():
    """Verify that document text is split into retrieval-friendly chunks."""

    document = {
        "source": "sample.pdf",
        "content": "A" * 2500,
    }

    chunks = chunk_text(
        document,
        chunk_size=1000,
        chunk_overlap=200,
    )

    assert len(chunks) == 4
    assert chunks[0]["source"] == "sample.pdf"
    assert chunks[0]["chunk_id"] == "sample.pdf_0"
    assert len(chunks[0]["content"]) == 1000


def test_chunk_text_rejects_invalid_overlap():
    """Verify that chunk overlap cannot be equal to or larger than chunk size."""

    document = {
        "source": "sample.pdf",
        "content": "Some sample content.",
    }

    with pytest.raises(ValueError):
        chunk_text(
            document,
            chunk_size=100,
            chunk_overlap=100,
        )


def test_parse_document_rejects_missing_file():
    """Verify that a missing document raises FileNotFoundError."""

    with pytest.raises(FileNotFoundError):
        parse_document("does_not_exist.pdf")


def test_parse_document_rejects_unsupported_format(tmp_path):
    """Verify that unsupported document formats are rejected."""

    unsupported_file = tmp_path / "sample.txt"
    unsupported_file.write_text("Sample content.")

    with pytest.raises(ValueError):
        parse_document(str(unsupported_file))


def test_embedder_rejects_empty_text():
    """Verify that empty text is rejected before an API call."""

    with patch("src.ingestion.embedder.OpenAI") as mock_openai:
        embedder = Embedder()

        with pytest.raises(ValueError):
            embedder.embed_text("")

        mock_openai.return_value.embeddings.create.assert_not_called()
