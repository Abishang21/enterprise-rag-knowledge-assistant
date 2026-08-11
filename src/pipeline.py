"""
Main RAG pipeline.

Coordinates document ingestion, vector indexing, retrieval,
and grounded response generation.
"""

from typing import Dict, List

from src.ingestion.document_parser import parse_document
from src.ingestion.chunker import chunk_text
from src.ingestion.embedder import Embedder
from src.retrieval.vector_store import FAISSVectorStore
from src.retrieval.retriever import Retriever
from src.generation.llm import LLMGenerator


class RAGPipeline:
    """End-to-end Retrieval-Augmented Generation pipeline."""

    def __init__(
        self,
        embedding_model: str = "text-embedding-3-small",
        llm_model: str = "gpt-4.1-mini",
    ):
        self.embedder = Embedder(model=embedding_model)
        self.llm = LLMGenerator(model=llm_model)

        self.vector_store = None
        self.retriever = None

    def index_document(
        self,
        file_path: str,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
    ) -> int:
        """
        Parse, chunk, embed, and index a document.

        Returns
        -------
        int
            Number of chunks indexed.
        """

        documents = parse_document(file_path)

        all_chunks: List[Dict] = []

        for document in documents:
            chunks = chunk_text(
                document,
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap,
            )

            all_chunks.extend(chunks)

        if not all_chunks:
            return 0

        embedded_chunks = self.embedder.embed_chunks(all_chunks)

        embedding_dimension = len(
            embedded_chunks[0]["embedding"]
        )

        if self.vector_store is None:
            self.vector_store = FAISSVectorStore(
                dimension=embedding_dimension
            )

        self.vector_store.add_documents(
            embedded_chunks
        )

        self.retriever = Retriever(
            vector_store=self.vector_store,
            embedder=self.embedder,
        )

        return len(embedded_chunks)

    def ask(
        self,
        query: str,
        top_k: int = 5,
    ) -> str:
        """
        Retrieve relevant context and generate a grounded answer.
        """

        if self.retriever is None:
            raise RuntimeError(
                "No knowledge has been indexed. "
                "Index at least one document before asking questions."
            )

        retrieved_context = self.retriever.retrieve(
            query=query,
            top_k=top_k,
        )

        return self.llm.generate(
            query=query,
            retrieved_context=retrieved_context,
        )
