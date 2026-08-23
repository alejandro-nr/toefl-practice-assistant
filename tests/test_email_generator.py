import json

import pytest

from toefl_practice_assistant.core.api_client import OpenRouterClient
from toefl_practice_assistant.writing.generators import EmailExerciseGenerator


@pytest.fixture
def sample_exercise_data() -> dict:
    return {
        "context": "You missed class yesterday.",
        "recipient": "Professor Smith",
        "objectives": ["Explain your absence", "Ask for lecture notes"],
        "bonus": ["Use formal greetings"],
    }


@pytest.fixture
def sample_api_response(sample_exercise_data) -> dict:
    return {
        "id": "gen-12345",
        "choices": [
            {
                "finish_reason": "stop",
                "message": {
                    "role": "assistant",
                    "content": json.dumps(sample_exercise_data),
                },
            }
        ],
        "model": "openai/gpt-4o",
    }


def test_build_payload_structure():
    system_prompt = "You are a TOEFL exercise generator."
    response_format = {"type": "json_object"}
    user_prompt = "Create an email about a missing book."
    model_name = "google/gemini-2.5-flash"
    api_client = OpenRouterClient(api_key="test-key")

    generator = EmailExerciseGenerator(
        model=model_name,
        system_prompt=system_prompt,
        response_format=response_format,
        api_client=api_client,
    )

    payload = generator.build_payload(user_prompt)

    assert payload["model"] == model_name
    assert payload["response_format"] == response_format
    assert payload["messages"] == [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]


def test_response_parsing(sample_exercise_data, sample_api_response):

    system_prompt = "You are a TOEFL exercise generator."
    response_format = {"type": "json_object"}
    model_name = "openai/gpt-4o"
    api_client = OpenRouterClient(api_key="test-key")
    generator = EmailExerciseGenerator(
        model=model_name,
        system_prompt=system_prompt,
        response_format=response_format,
        api_client=api_client,
    )

    parsed = generator.parse_response(sample_api_response)
    assert parsed.context == sample_exercise_data["context"]
    assert parsed.recipient == sample_exercise_data["recipient"]
    assert parsed.objectives == sample_exercise_data["objectives"]
    assert parsed.bonus == sample_exercise_data["bonus"]


def test_generate(mocker, sample_api_response, sample_exercise_data):
    mock_client = mocker.Mock()
    mock_client.post.return_value = sample_api_response

    system_prompt = "You are a TOEFL exercise generator."
    response_format = {"type": "json"}
    model_name = "gpt-4o"
    generator = EmailExerciseGenerator(
        model=model_name,
        system_prompt=system_prompt,
        response_format=response_format,
        api_client=mock_client,
    )

    user_prompt = "Generate a new exercise."
    exercise = generator.generate(user_prompt)

    expected_payload = generator.build_payload(user_prompt)
    mock_client.post.assert_called_once_with(expected_payload)

    assert exercise.context == sample_exercise_data["context"]
    assert exercise.recipient == sample_exercise_data["recipient"]
    assert exercise.objectives == sample_exercise_data["objectives"]
    assert exercise.bonus == sample_exercise_data["bonus"]
