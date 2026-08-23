from typing import Any

from toefl_practice_assistant.core.api_client import OpenRouterClient


class LLMChatSession:
    def __init__(
        self,
        api_client: OpenRouterClient,
        model: str,
        system_prompt: str,
    ) -> None:
        self.api_client = api_client
        self.model = model
        self.system_prompt = system_prompt
        self.messages = [{"role": "system", "content": system_prompt}]

    def send_message(self, message: str) -> str:
        self.messages.append({"role": "user", "content": message})

        payload = self.build_payload()
        response_data = self.api_client.post(payload)

        assistant_response = response_data["choices"][0]["message"]["content"]
        self.messages.append({"role": "assistant", "content": assistant_response})

        return assistant_response

    def build_payload(self) -> dict[str, Any]:
        return {
            "model": self.model,
            "messages": self.messages,
        }
