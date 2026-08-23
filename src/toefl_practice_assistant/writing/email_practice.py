import tkinter as tk
from tkinter import ttk

from toefl_practice_assistant.core.gui_tools import LabeledCombobox, LabeledEntry


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


class ApiConfigFrame(ttk.Frame):
    """Custom widget to configure options related to the OpenRouter API."""

    def __init__(self, parent: tk.Misc, model_options: list[str]) -> None:
        super().__init__(parent)
        self.columnconfigure(index=0, weight=1)

        self.api_entry = LabeledEntry(
            parent=self,
            label_text="API key",
            label_width=5,
            show="*",
        )
        self.api_entry.grid(row=0, column=0, sticky="we", padx=2, pady=5)

        self.show_api_key = tk.BooleanVar(value=False)
        self.visibility_checkbutton = ttk.Checkbutton(
            self,
            text="show key",
            command=self.change_visibility,
            variable=self.show_api_key,
        )
        self.visibility_checkbutton.grid(row=0, column=1, sticky="we", padx=2, pady=5)

        self.model_combobox = LabeledCombobox(
            parent=self,
            text="Model",
            label_width=5,
            combobox_width=10,
            choices=model_options,
        )
        self.model_combobox.grid(row=1, column=0, sticky="we", padx=2, pady=5)

    def get_api_key(self) -> str:
        """Returns the current value of the api key entry."""
        return self.api_entry.get()

    def get_model(self) -> str:
        """Returns the selected model."""
        return self.model_combobox.get_choice()

    def change_visibility(self) -> None:
        """Configures the visibility of the api-key according to the visibility_checkbutton"""
        if self.show_api_key.get():
            self.api_entry.set_show(char="")
        else:
            self.api_entry.set_show(char="*")


class PromptsConfigFrame(ttk.Frame):
    """Custom widget to configure prompt related options, like user prompt for text generation and tags for talking with the assistant."""

    def __init__(
        self, parent: tk.Misc, default_prompt: str = "Generate a new email exercise."
    ) -> None:
        super().__init__(parent)
        self.columnconfigure(index=0, weight=1)
        self.rowconfigure(index=1, weight=1)

        tags_frame = ttk.LabelFrame(self, text="Tags for talking with the assistant:")
        tags_frame.columnconfigure(index=0, weight=1)
        tags_frame.grid(row=0, column=0, sticky="we", padx=5, pady=5)

        self.exercise_tag_entry = LabeledEntry(
            parent=tags_frame,
            label_text="Exercise tag",
            label_width=10,
            initial_entry_text="[EX]",
        )
        self.exercise_tag_entry.grid(row=0, column=0, sticky="we", padx=2, pady=5)

        self.solution_tag_entry = LabeledEntry(
            parent=tags_frame,
            label_text="Solution tag",
            label_width=10,
            initial_entry_text="[SOL]",
        )
        self.solution_tag_entry.grid(row=1, column=0, sticky="we", padx=2, pady=5)

        generation_prompts_frame = ttk.LabelFrame(
            self, text="Prompt for exercise generation:"
        )
        generation_prompts_frame.rowconfigure(index=0, weight=1)
        generation_prompts_frame.columnconfigure(index=0, weight=1)
        generation_prompts_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

        self.prompt_textbox = tk.Text(
            generation_prompts_frame,
            width=50,
            height=5,
            wrap="word",
        )
        self.prompt_textbox.grid(row=0, column=0, sticky="nswe", padx=5)
        self.prompt_textbox.insert("1.0", default_prompt)

    def get_exercise_generation_prompt(self) -> str:
        return self.prompt_textbox.get("1.0", tk.END).strip()

    def get_exercise_tag(self) -> str:
        return self.exercise_tag_entry.get()

    def get_solution_tag(self) -> str:
        return self.solution_tag_entry.get()


if __name__ == "__main__":
    root = tk.Tk()
    root.rowconfigure(index=0, weight=1)
    root.columnconfigure(index=0, weight=1)

    # instructions_frame = InstructionsFrame(root)
    # instructions_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    # api_config_frame = ApiConfigFrame(root, model_options=["Gemini", "GPT", "Claude"])
    # api_config_frame.grid(row=0, column=0, sticky="we", padx=5, pady=5)

    prompts_config_frame = PromptsConfigFrame(root)
    prompts_config_frame.grid(row=0, column=0, sticky="nswe", padx=5, pady=5)

    root.mainloop()
