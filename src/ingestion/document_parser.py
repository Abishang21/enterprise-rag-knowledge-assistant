"""
Document parsing module for the private RAG knowledge system.

This module extracts structured text from supported document formats
while keeping the ingestion pipeline separate from retrieval and
generation components.
"""

from pathlib import Path
from typing import List, Dict

from docling.document_converter import DocumentConverter


SUPPORTED_EXTENSIONS = {".pdf", ".docx"}


def parse_document(file_path: str) -> List[Dict]:
    """
    Parse a document and return structured content.

    Parameters
    ----------
    file_path : str
        Path to the PDF or DOCX document.

    Returns
    -------
    List[Dict]
        Parsed document content with basic metadata.

    Raises
    ------
    FileNotFoundError
        If the specified document does not exist.

    ValueError
        If the document format is not supported.
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Document not found: {file_path}")

    if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
        raise ValueError(
            f"Unsupported document format: {path.suffix}. "
            f"Supported formats: {SUPPORTED_EXTENSIONS}"
        )

    converter = DocumentConverter()

    result = converter.convert(str(path))

    document = result.document

    markdown_content = document.export_to_markdown()

    return [
        {
            "source": path.name,
            "content": markdown_content,
            "file_type": path.suffix.lower(),
        }
    ]


if __name__ == "__main__":
    print("Document parser module loaded successfully.")
