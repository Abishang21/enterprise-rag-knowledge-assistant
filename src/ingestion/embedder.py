"""
Embedding module for the RAG knowledge system.

Converts document chunks into vector representations that can
be indexed and searched for semantic similarity.
"""

from typing import Dict, List

from openai import OpenAI


class Embedder:
    """Generate embeddings for document chunks."""

    def __init__(
        self,
        model: str = "text-embedding-3-small",
    ):
        self.client = OpenAI()
        self.model = model

    def embed_text(self, text: str) -> List[float]:
        """
        Generate an embedding for a single text string.
        """

        if not text.strip():
            raise ValueError("Cannot generate an embedding for empty text.")

        response = self.client.embeddings.create(
            model=self.model,
            input=text,
        )

        return response.data[0].embedding

    def embed_chunks(self, chunks: List[Dict]) -> List[Dict]:
        """
        Generate embeddings for a list of document chunks.
        """

        embedded_chunks = []

        for chunk in chunks:
            embedding = self.embed_text(chunk["content"])

            embedded_chunks.append(
                {
                    **chunk,
                    "embedding": embedding,
                }
            )

        return embedded_chunks
