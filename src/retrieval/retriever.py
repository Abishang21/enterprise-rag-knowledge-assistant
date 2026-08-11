"""
Retrieval module for the RAG knowledge system.

Converts a user query into an embedding and retrieves
the most relevant knowledge chunks from the vector store.
"""

from typing import Dict, List

from src.ingestion.embedder import Embedder
from src.retrieval.vector_store import FAISSVectorStore


class Retriever:
    """Retrieve relevant knowledge from the vector store."""

    def __init__(
        self,
        vector_store: FAISSVectorStore,
        embedder: Embedder,
    ):
        self.vector_store = vector_store
        self.embedder = embedder

    def retrieve(
        self,
        query: str,
        top_k: int = 5,
    ) -> List[Dict]:
        """
        Retrieve the most relevant chunks for a user query.

        Parameters
        ----------
        query : str
            User's natural-language question.

        top_k : int
            Number of relevant chunks to retrieve.

        Returns
        -------
        List[Dict]
            Retrieved chunks with similarity distances.
        """

        if not query.strip():
            raise ValueError("Query cannot be empty.")

        query_embedding = self.embedder.embed_text(query)

        search_results = self.vector_store.search(
            query_embedding=query_embedding,
            top_k=top_k,
        )

        return [
            {
                **document,
                "distance": distance,
            }
            for document, distance in search_results
        ]
