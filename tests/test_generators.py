from toefl_writing_prep.generators import EmailExerciseGenerator
from toefl_writing_prep.models import EmailExercise
import json

def test_build_payload_structure():
    system_prompt = "You are a TOEFL exercise generator."
    response_format = {"type": "json_object"}
    user_prompt = "Create an email about a missing book."
    model_name = "google/gemini-2.5-flash"

    generator = EmailExerciseGenerator(
        model=model_name,
        system_prompt=system_prompt,
        response_format=response_format,
    )

    payload = generator.build_payload(user_prompt)

    assert payload["model"] == model_name
    assert payload["response_format"] == response_format
    assert payload["messages"] == [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]



def test_response_parsing():

    system_prompt = "You are a TOEFL exercise generator."
    response_format = {"type": "json_object"}
    model_name = "openai/gpt-4o"
    generator = EmailExerciseGenerator(
        model=model_name,
        system_prompt=system_prompt,
        response_format=response_format,
    )

    exercise_data = {
        "context": "You missed class yesterday.",
        "recipient": "Professor Smith",
        "objectives": ["Explain your absence", "Ask for lecture notes"],
        "bonus": ["Use formal greetings"],
    }
    response_data = {
        "id": "gen-xxxxxxxxxxxxxx",
        "choices": [
            {
                "finish_reason": "stop",
                "native_finish_reason": "stop",
                "message": {
                    "role": "assistant",
                    "content": json.dumps(exercise_data),
                },
            }
        ],
        "usage": {
            "prompt_tokens": 10,
            "completion_tokens": 4,
            "total_tokens": 14,
            "prompt_tokens_details": {"cached_tokens": 0},
            "completion_tokens_details": {"reasoning_tokens": 0},
            "cost": 0.00014,
        },
        "model": f"{model_name}",
    }

    parsed = generator.parse_response(response_data)
    assert parsed.context == exercise_data["context"]
    assert parsed.recipient == exercise_data["recipient"]
    assert parsed.objectives == exercise_data["objectives"]
    assert parsed.bonus == exercise_data["bonus"]
