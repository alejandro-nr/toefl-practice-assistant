import pytest

from toefl_practice_assistant.core.api_client import OpenRouterClient
from toefl_practice_assistant.core.llm_chat import LLMChatSession


@pytest.fixture
def sample_api_response() -> dict:
    return {
        "id": "gen-12345",
        "choices": [
            {
                "finish_reason": "stop",
                "message": {
                    "role": "assistant",
                    "content": "Sample response text from the OpenRouter API.",
                },
            }
        ],
        "model": "google/gemini-3.7-flash",
    }


def test_session_initialization():

    api_key = "test-key-123"
    model = "google/gemini-3.7-flash"
    system_prompt = "You are a helpful coding assistant."

    api_client = OpenRouterClient(api_key=api_key)
    chat_session = LLMChatSession(
        api_client,
        model,
        system_prompt,
    )

    assert isinstance(chat_session.api_client, OpenRouterClient)
    assert chat_session.api_client.api_key == api_key
    assert chat_session.model == model
    assert chat_session.system_prompt == system_prompt
    assert chat_session.messages == [{"role": "system", "content": system_prompt}]


def test_build_payload(mocker):
    mock_client = mocker.Mock()
    model = "google/gemini-3.7-flash"
    system_prompt = "You are a helpful coding assistant."

    chat_session = LLMChatSession(
        api_client=mock_client,
        model=model,
        system_prompt=system_prompt,
    )

    chat_session.messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": "Can you explain python classes"},
        {"role": "assistant", "content": "Sure! Python classes are..."},
        {"role": "user", "content": "Thanks! Now, what is pytest for?"},
        {"role": "assistant", "content": "Pytest is a library for testing..."},
    ]

    payload = chat_session.build_payload()

    assert payload == {
        "model": model,
        "messages": chat_session.messages,
    }


def test_send_message(mocker, sample_api_response):
    mock_client = mocker.Mock()
    mock_client.post.return_value = sample_api_response

    assistant_response = sample_api_response["choices"][0]["message"]["content"]

    model = "google/gemini-3.7-flash"
    system_prompt = "You are a helpful coding assistant."
    chat_session = LLMChatSession(
        api_client=mock_client,
        model=model,
        system_prompt=system_prompt,
    )

    first_message = "What is a for loop in python?"
    response_1 = chat_session.send_message(message=first_message)

    assert response_1 == assistant_response
    assert len(chat_session.messages) == 3
    assert chat_session.messages[-2] == {
        "role": "user",
        "content": first_message,
    }
    assert chat_session.messages[-1] == {
        "role": "assistant",
        "content": assistant_response,
    }

    second_message = "Can you explain what is a python function"
    response_2 = chat_session.send_message(message=second_message)

    assert response_2 == assistant_response
    assert len(chat_session.messages) == 5
    assert chat_session.messages[-2] == {
        "role": "user",
        "content": second_message,
    }
    assert chat_session.messages[-1] == {
        "role": "assistant",
        "content": assistant_response,
    }
