"""
Tests for the enterprise API retrieval layer.
"""

from unittest.mock import Mock, patch

from src.enterprise.api_retriever import EnterpriseAPIRetriever


def test_enterprise_api_search():
    """Verify that an authenticated API search returns JSON data."""

    mock_response = Mock()

    mock_response.json.return_value = {
        "query": "employee engagement",
        "results": [
            {
                "id": "DOC-001",
                "title": "Employee Engagement Policy",
                "content": "Annual employee engagement survey."
            }
        ],
        "count": 1,
    }

    mock_response.raise_for_status.return_value = None

    with patch(
        "src.enterprise.api_retriever.requests.get",
        return_value=mock_response,
    ) as mock_get:

        retriever = EnterpriseAPIRetriever(
            base_url="https://mock-enterprise-api.example.com",
            api_token="test-token",
        )

        result = retriever.search(
            "employee engagement"
        )

        assert result["count"] == 1
        assert result["results"][0]["id"] == "DOC-001"

        mock_get.assert_called_once()
