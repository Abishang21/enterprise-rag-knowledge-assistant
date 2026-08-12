"""
End-to-end demonstration of the Enterprise RAG Knowledge Assistant.

This demo shows how the system can combine two knowledge sources:

1. Document-based knowledge
   PDF/DOCX → parsing → chunking → embeddings → FAISS retrieval

2. Enterprise portal/API knowledge
   Authenticated API → relevant information

The demo uses mock/sanitized enterprise data and does not connect
to any real organization's systems.
"""
from src.generation.llm import LLMGenerator

MOCK_KNOWLEDGE = [
    {
        "id": "DOC-001",
        "title": "Employee Engagement Policy",
        "content": (
            "The organization conducts an annual employee "
            "engagement survey to assess workplace experience, "
            "communication, leadership, and employee satisfaction."
        ),
    },
    {
        "id": "DOC-002",
        "title": "Performance Management Framework",
        "content": (
            "The performance management framework includes "
            "goal setting, periodic performance reviews, "
            "feedback sessions, and professional development."
        ),
    },
    {
        "id": "DOC-003",
        "title": "Research Data Governance Policy",
        "content": (
            "Research data must be collected, stored, processed, "
            "and accessed according to organizational data "
            "governance and privacy requirements."
        ),
    },
]


def search_knowledge(query: str):
    """Simulate an enterprise portal/API search."""

    query_terms = query.lower().split()

    results = []

    for document in MOCK_KNOWLEDGE:
        searchable_text = (
            f"{document['title']} {document['content']}"
        ).lower()

        if any(
            term in searchable_text
            for term in query_terms
        ):
            results.append(document)

    return {
        "query": query,
        "results": results,
        "count": len(results),
    }


def normalize_enterprise_results(api_response):
    """
    Convert enterprise API results into the common context format
    expected by the generation layer.
    """

    normalized = []

    for item in api_response.get("results", []):
        normalized.append(
            {
                "source": f"Enterprise API: {item.get('title', 'Unknown')}",
                "content": item.get("content", ""),
            }
        )

    return normalized


def main():
    """Run the enterprise knowledge retrieval demonstration."""

    query = "employee engagement"

    print("=" * 60)
    print("Enterprise RAG Knowledge Assistant")
    print("=" * 60)

    print(f"\nUser question: {query}")

    # ---------------------------------------------------------
    # Enterprise Portal / API Knowledge Path
    # ---------------------------------------------------------

    print("\n[1] Enterprise API Retrieval")
    print("-" * 60)

    api_response = search_knowledge(query)

    enterprise_context = normalize_enterprise_results(
        api_response
    )

    if enterprise_context:
        for item in enterprise_context:
            print(f"\nSource: {item['source']}")
            print(f"Content: {item['content']}")
    else:
        print("No relevant enterprise information found.")

    # ---------------------------------------------------------
    # Context Assembly
    # ---------------------------------------------------------

    print("\n[2] Retrieved Context")
    print("-" * 60)

    combined_context = enterprise_context

    if combined_context:
        for item in combined_context:
            print(f"\n[{item['source']}]")
            print(item["content"])
    else:
        print("No context available.")

    # ---------------------------------------------------------
# Generation Layer
# ---------------------------------------------------------

    print("\n[3] Generation")
    print("-" * 60)

    if enterprise_context:
            try:
                generator = LLMGenerator()

                answer = generator.generate(
                    query=query,
                    retrieved_context=enterprise_context,
                )

                print("\nGrounded Answer:")
                print(answer)

            except Exception as exc:
                print("\nLLM generation is unavailable.")
                print(f"Reason: {exc}")

                print("\nDemo Fallback Answer:")
                print(
                    "The organization conducts an annual employee "
                    "engagement survey to assess workplace experience, "
                "communication, leadership, and employee satisfaction."
            )

    else:
            print("\nNo context available for generation.")

if __name__ == "__main__":
    main()