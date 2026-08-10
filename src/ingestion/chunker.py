"""
Text chunking module for the RAG knowledge system.

Responsible for dividing parsed documents into smaller,
retrieval-friendly units while preserving source metadata.
"""

from typing import Dict, List


def chunk_text(
    document: Dict,
    chunk_size: int = 1000,
    chunk_overlap: int = 200,
) -> List[Dict]:
    """
    Split document content into overlapping chunks.

    Parameters
    ----------
    document : Dict
        Parsed document containing source metadata and content.

    chunk_size : int
        Maximum approximate size of each chunk.

    chunk_overlap : int
        Number of characters shared between consecutive chunks.

    Returns
    -------
    List[Dict]
        A list of chunks with source and chunk metadata.
    """

    content = document.get("content", "")
    source = document.get("source", "unknown")

    if not content.strip():
        return []

    if chunk_overlap >= chunk_size:
        raise ValueError("chunk_overlap must be smaller than chunk_size.")

    chunks = []

    start = 0
    chunk_index = 0

    while start < len(content):
        end = start + chunk_size

        chunk = content[start:end].strip()

        if chunk:
            chunks.append(
                {
                    "chunk_id": f"{source}_{chunk_index}",
                    "source": source,
                    "content": chunk,
                }
            )

        chunk_index += 1
        start = end - chunk_overlap

    return chunks
