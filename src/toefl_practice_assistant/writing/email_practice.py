import tkinter as tk
from tkinter import ttk


class InstructionsFrame(ttk.Frame):
    """Custom widget that holds the instructions for an email exercise."""

    def __init__(self, parent: tk.Misc) -> None:
        super().__init__(parent)
        self.rowconfigure(index=0, weight=1)
        self.columnconfigure(index=0, weight=1)

        self.exercise_textbox = tk.Text(
            self,
            width=50,
            padx=5,
            pady=5,
            font=("Arial", 14),
            wrap="word",
        )
        self.exercise_textbox.grid(row=0, column=0, sticky="nsew")

        self.edition_enabled = tk.BooleanVar(value=False)
        self.edition_checkbutton = ttk.Checkbutton(
            self,
            onvalue=True,
            offvalue=False,
            text="Allow edition",
            variable=self.edition_enabled,
            command=self.on_checkbutton,
        )
        self.edition_checkbutton.grid(row=1, column=0, sticky="e")

        self.exercise_textbox.insert("1.0", "No exercise loaded...")
        self.exercise_textbox.configure(state="disabled")

    def on_checkbutton(self) -> None:
        """Checks the value of the edition_checkbutton and updates the state of the textbox."""
        textbox_state = "normal" if self.edition_enabled.get() else "disabled"
        self.exercise_textbox.configure(state=textbox_state)

    def get_exercise(self) -> str:
        """Returns the current text from the exercise_textbox."""
        return self.exercise_textbox.get("1.0", tk.END)

    def set_exercise(self, text: str) -> None:
        """Inserts a new exercise into the textbox."""
        self.exercise_textbox.configure(state="normal")
        self.exercise_textbox.delete("1.0", tk.END)
        self.exercise_textbox.insert("1.0", text)
        self.on_checkbutton()


if __name__ == "__main__":
    root = tk.Tk()
    root.rowconfigure(index=0, weight=1)
    root.columnconfigure(index=0, weight=1)

    instructions_frame = InstructionsFrame(root)
    instructions_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    root.mainloop()
