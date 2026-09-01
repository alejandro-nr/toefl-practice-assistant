from toefl_practice_assistant.writing.models import EmailExercise


def test_email_exercise_from_dict():
    data = {
        "context": "You missed class yesterday.",
        "recipient": "Professor Smith",
        "objectives": ["Explain your absence", "Ask for lecture notes"],
    }

    exercise = EmailExercise.from_dict(data)

    assert exercise.context == data["context"]
    assert exercise.recipient == data["recipient"]
    assert exercise.objectives == data["objectives"]


def test_email_exercise_str_formatting():
    exercise = EmailExercise(
        context="You missed class yesterday.",
        recipient="Professor Smith",
        objectives=["Explain your absence", "Ask for lecture notes"],
    )

    expected_output = (
        "You missed class yesterday.\n\n"
        "Write an email to Professor Smith. In your email do the following:\n"
        "  - Explain your absence\n"
        "  - Ask for lecture notes"
    )

    assert str(exercise) == expected_output
