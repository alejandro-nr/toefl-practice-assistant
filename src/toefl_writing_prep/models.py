class EmailExercise:
    def __init__(
        self, context: str, recipient: str, objectives: list[str], bonus: list[str]
    ):
        self.context = context
        self.recipient = recipient
        self.objectives = objectives
        self.bonus = bonus

    def __str__(self):
        s = self.context
        s += (
            f"\n\nWrite an email to {self.recipient}. In your email do the following:\n"
        )
        for objective in self.objectives:
            s += "  - " + objective + "\n"
        s += "\nBonus points if you do the following:\n"
        for challenge in self.bonus:
            s += "  - " + challenge + "\n"
        return s.strip()
