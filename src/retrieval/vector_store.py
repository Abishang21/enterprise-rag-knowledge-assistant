"""
FAISS vector store for the RAG knowledge system.

Stores document embeddings locally and provides similarity
search over indexed knowledge chunks.
"""

from pathlib import Path
from typing import Dict, List, Tuple

import faiss
import numpy as np


class FAISSVectorStore:
    """Local FAISS-based vector store."""

    def __init__(self, dimension: int):
        self.dimension = dimension
        self.index = faiss.IndexFlatL2(dimension)
        self.documents: List[Dict] = []

    def add_documents(self, embedded_chunks: List[Dict]) -> None:
        """
        Add embedded document chunks to the FAISS index.
        """

        if not embedded_chunks:
            return

        vectors = np.array(
            [chunk["embedding"] for chunk in embedded_chunks],
            dtype="float32",
        )

        if vectors.shape[1] != self.dimension:
            raise ValueError(
                f"Embedding dimension {vectors.shape[1]} "
                f"does not match index dimension {self.dimension}."
            )

        self.index.add(vectors)

        self.documents.extend(
            {
                key: value
                for key, value in chunk.items()
                if key != "embedding"
            }
            for chunk in embedded_chunks
        )

    def search(
        self,
        query_embedding: List[float],
        top_k: int = 5,
    ) -> List[Tuple[Dict, float]]:
        """
        Search for the most similar document chunks.
        """

        if not self.documents:
            return []

        query_vector = np.array(
            [query_embedding],
            dtype="float32",
        )

        distances, indices = self.index.search(
            query_vector,
            min(top_k, len(self.documents)),
        )

        results = []

        for distance, index in zip(distances[0], indices[0]):
            if index == -1:
                continue

            results.append(
                (
                    self.documents[index],
                    float(distance),
                )
            )

        return results

    def save(self, directory: str) -> None:
        """
        Save the FAISS index locally.
        """

        path = Path(directory)
        path.mkdir(parents=True, exist_ok=True)

        faiss.write_index(
            self.index,
            str(path / "knowledge.index"),
        )

        np.save(
            path / "documents.npy",
            np.array(self.documents, dtype=object),
            allow_pickle=True,
        )

    def load(self, directory: str) -> None:
        """
        Load a previously saved FAISS index.
        """

        path = Path(directory)

        self.index = faiss.read_index(
            str(path / "knowledge.index")
        )

        self.documents = np.load(
            path / "documents.npy",
            allow_pickle=True,
        ).tolist()
