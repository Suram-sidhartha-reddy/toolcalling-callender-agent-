from typing import Any

import httpx

from client.config import API_BASE_URL, API_TIMEOUT


class APIError(Exception):
    """Raised when the Calendar Agent API returns an error."""

    def __init__(
        self,
        message: str,
        status_code: int | None = None,
    ):
        super().__init__(message)
        self.status_code = status_code


class CalendarAPIClient:
    """
    HTTP client for the Calendar AI Agent API.
    """

    def __init__(
        self,
        base_url: str = API_BASE_URL,
        timeout: float = API_TIMEOUT,
    ):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def health_check(self) -> dict[str, Any]:
        """
        Check whether the API server is running.
        """

        try:
            response = httpx.get(
                f"{self.base_url}/",
                timeout=self.timeout,
            )

        except httpx.RequestError as exc:
            raise APIError(
                f"Could not connect to API: {exc}"
            ) from exc

        if response.status_code >= 400:
            raise APIError(
                f"Health check failed: {response.text}",
                response.status_code,
            )

        return response.json()

    def chat(
        self,
        message: str,
        source: str = "user_command",
        sender: str | None = None,
    ) -> dict[str, Any]:
        """
        Send a message to the Calendar AI Agent.
        """

        payload = {
            "message": message,
            "source": source,
            "sender": sender,
        }

        try:
            response = httpx.post(
                f"{self.base_url}/chat",
                json=payload,
                timeout=self.timeout,
            )

        except httpx.RequestError as exc:
            raise APIError(
                f"Could not connect to API: {exc}"
            ) from exc

        if response.status_code >= 400:
            raise APIError(
                f"API request failed: {response.text}",
                response.status_code,
            )

        return response.json()