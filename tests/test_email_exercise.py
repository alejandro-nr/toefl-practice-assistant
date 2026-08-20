from toefl_writing_prep.models import EmailExercise


def test_email_exercise_str_formatting():
    exercise = EmailExercise(
        context="You missed class yesterday.",
        recipient="Professor Smith",
        objectives=["Explain your absence", "Ask for lecture notes"],
        bonus=["Use formal greetings", "Keep it under 100 words"],
    )

    expected_output = (
        "You missed class yesterday.\n\n"
        "Write an email to Professor Smith. In your email do the following:\n"
        "  - Explain your absence\n"
        "  - Ask for lecture notes\n\n"
        "Bonus points if you do the following:\n"
        "  - Use formal greetings\n"
        "  - Keep it under 100 words"
    )

    assert str(exercise) == expected_output
