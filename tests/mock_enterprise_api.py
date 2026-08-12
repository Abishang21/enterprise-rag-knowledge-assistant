"""
Mock enterprise API for testing.

This simulated API represents an authenticated enterprise
knowledge source without connecting to any real organization
or proprietary system.
"""

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
    """
    Simulate an enterprise knowledge search endpoint.
    """

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
