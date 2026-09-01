from typing import Any


class EmailExercise:
    def __init__(
        self,
        context: str,
        recipient: str,
        objectives: list[str],
    ):
        self.context = context
        self.recipient = recipient
        self.objectives = objectives

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "EmailExercise":
        """Creates an EmailExercise instance from a dictionary."""
        return cls(
            context=data["context"],
            recipient=data["recipient"],
            objectives=data["objectives"],
        )

    def __str__(self):
        s = self.context
        s += (
            f"\n\nWrite an email to {self.recipient}. In your email do the following:\n"
        )
        for objective in self.objectives:
            s += "  - " + objective + "\n"

        return s.strip()
