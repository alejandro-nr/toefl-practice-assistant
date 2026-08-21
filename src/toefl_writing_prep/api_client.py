from typing import Any

import requests


class OpenRouterClient:
    """Client to handle HTTP communication with the OpenRouter API."""

    COMPLETIONS_URL: str = "https://openrouter.ai/api/v1/chat/completions"

    def __init__(
        self,
        api_key: str,
        api_url: str = COMPLETIONS_URL,
    ) -> None:
        self.api_key = api_key
        self.api_url = api_url
        self.headers: dict[str, str] = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def post(self, payload: dict[str, Any]) -> dict[str, Any]:
        """Sends a POST request to OpenRouter and returns the parsed JSON."""
        response = requests.post(self.api_url, headers=self.headers, json=payload)
        return response.json()
