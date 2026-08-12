"""
Enterprise API retrieval module.

Provides a controlled interface for retrieving knowledge from
authenticated enterprise portals and APIs.

This module is designed as an abstraction layer so that the
RAG system does not need to know the implementation details
of the underlying enterprise system.
"""

from typing import Any, Dict, Optional

import requests


class EnterpriseAPIRetriever:
    """
    Retrieve authorized information from an enterprise API.
    """

    def __init__(
        self,
        base_url: str,
        api_token: Optional[str] = None,
        timeout: int = 30,
    ):
        self.base_url = base_url.rstrip("/")
        self.api_token = api_token
        self.timeout = timeout

    def _headers(self) -> Dict[str, str]:
        """
        Build authentication headers.
        """

        headers = {
            "Accept": "application/json",
        }

        if self.api_token:
            headers["Authorization"] = (
                f"Bearer {self.api_token}"
            )

        return headers

    def search(
        self,
        query: str,
        endpoint: str = "/search",
    ) -> Dict[str, Any]:
        """
        Search the enterprise knowledge system.

        Parameters
        ----------
        query : str
            User's search query.

        endpoint : str
            API endpoint used for searching.

        Returns
        -------
        Dict[str, Any]
            API response containing relevant information.
        """

        if not query.strip():
            raise ValueError("Query cannot be empty.")

        url = f"{self.base_url}{endpoint}"

        response = requests.get(
            url,
            headers=self._headers(),
            params={"q": query},
            timeout=self.timeout,
        )

        response.raise_for_status()

        return response.json()

    def get(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Retrieve information from a specific enterprise API endpoint.
        """

        url = f"{self.base_url}{endpoint}"

        response = requests.get(
            url,
            headers=self._headers(),
            params=params,
            timeout=self.timeout,
        )

        response.raise_for_status()

        return response.json()
