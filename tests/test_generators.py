from toefl_writing_prep.generators import EmailExerciseGenerator


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
