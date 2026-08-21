from toefl_writing_prep.models import EmailExercise
from typing import Any
import json


class EmailExerciseGenerator:
    """Generates TOEFL email writing exercises using an LLM."""

    def __init__(
        self,
        model: str,
        system_prompt: str,
        response_format: dict[str, Any],
    ) -> None:
        self.model = model
        self.system_prompt = system_prompt
        self.response_format = response_format

    def build_payload(self, user_prompt: str) -> dict[str, Any]:
        """Constructs the payload dictionary for the OpenRouter API."""
        return {
            "model": self.model,
            "messages": [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "response_format": self.response_format,
        }

    def set_model(self, new_model: str) -> None:
        """Updates the target LLM model."""
        self.model = new_model

    def parse_response(self, response_data: dict[str, Any]) -> EmailExercise:
        """Parses the response from the API into an EmailExercise object."""
        try:
            content = response_data["choices"][0]["message"]["content"]
            exercise_data = json.loads(content)
            return EmailExercise.from_dict(exercise_data)
        except (KeyError, IndexError, json.JSONDecodeError) as e:
            raise ValueError(f"Invalid API response format: {e}") from e
