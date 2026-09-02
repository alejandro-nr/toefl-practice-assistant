import tkinter as tk
from collections.abc import Callable
from tkinter import ttk

from toefl_practice_assistant.core.api_client import OpenRouterClient
from toefl_practice_assistant.core.chat_gui import LLMChatFrame
from toefl_practice_assistant.core.gui_tools import LabeledCombobox, LabeledEntry
from toefl_practice_assistant.core.llm_chat import LLMChatSession
from toefl_practice_assistant.core.timer import TimerFrame
from toefl_practice_assistant.writing.generators import (
    EmailExerciseGenerator,
)
from toefl_practice_assistant.writing.prompts import (
    EMAIL_ASSISTANT_SYSTEM_PROMPT,
    EMAIL_GENERATION_FORMAT,
    EMAIL_GENERATOR_SYSTEM_PROMPT,
)


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
        self.exercise_textbox.grid(row=0, column=0, columnspan=2, sticky="nsew")

        self.edition_enabled = tk.BooleanVar(value=False)
        self.edition_checkbutton = ttk.Checkbutton(
            self,
            onvalue=True,
            offvalue=False,
            text="Allow edition",
            variable=self.edition_enabled,
            command=self.on_checkbutton,
        )
        self.edition_checkbutton.grid(row=1, column=1, sticky="e", pady=5)

        self.generate_button = ttk.Button(self, text="generate")
        self.generate_button.grid(row=1, column=0, sticky="e", padx=5, pady=5)

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

    def set_generate_command(self, callback: Callable[[], None]) -> None:
        """Sets or updates the generate button command callback."""
        self.generate_button.configure(command=callback)


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
        self.api_entry.grid(row=0, column=0, columnspan=2, sticky="we", padx=2, pady=2)

        self.show_api_key = tk.BooleanVar(value=False)
        self.visibility_checkbutton = ttk.Checkbutton(
            self,
            text="show key",
            command=self.change_visibility,
            variable=self.show_api_key,
        )
        self.visibility_checkbutton.grid(row=1, column=0, sticky="e", padx=2)

        self.api_button = ttk.Button(self, text="save key")
        self.api_button.grid(row=1, column=1, sticky="e", padx=2)

        self.model_combobox = LabeledCombobox(
            parent=self,
            text="Model",
            label_width=5,
            combobox_width=10,
            choices=model_options,
        )
        self.model_combobox.grid(
            row=2, column=0, columnspan=2, sticky="we", padx=5, pady=5
        )

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

    def set_api_button_command(self, callback: Callable[[], None]) -> None:
        """Sets or updates the api button command callback."""
        self.api_button.configure(command=callback)


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
            initial_entry_text="EE",
        )
        self.exercise_tag_entry.grid(row=0, column=0, sticky="we", padx=2, pady=5)

        self.solution_tag_entry = LabeledEntry(
            parent=tags_frame,
            label_text="Solution tag",
            label_width=10,
            initial_entry_text="SS",
        )
        self.solution_tag_entry.grid(row=1, column=0, sticky="we", padx=2, pady=5)

        generation_prompts_frame = ttk.LabelFrame(
            self, text="Prompt for exercise generation:"
        )
        generation_prompts_frame.rowconfigure(index=4, weight=1)
        generation_prompts_frame.columnconfigure(index=0, weight=1)
        generation_prompts_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

        self.prompt_register_combobox = LabeledCombobox(
            parent=generation_prompts_frame,
            text="Register",
            label_width=12,
            combobox_width=10,
            choices=["formal", "informal"],
        )
        self.prompt_register_combobox.grid(row=0, column=0, sticky="we", padx=5, pady=2)

        self.prompt_objective_combobox = LabeledCombobox(
            parent=generation_prompts_frame,
            text="Objective",
            label_width=12,
            combobox_width=10,
            choices=[
                "giving advice",
                "making an invitation",
                "proposing a solution",
                "requesting information",
                "resolving a logistical issue",
                "addressing a campus service or resource",
                "cancelling something",
                "notifying someone of a change",
                "apologizing for something",
            ],
        )
        self.prompt_objective_combobox.grid(
            row=1, column=0, sticky="we", padx=5, pady=2
        )

        self.prompt_difficulty_combobox = LabeledCombobox(
            parent=generation_prompts_frame,
            text="Difficulty",
            label_width=12,
            combobox_width=10,
            choices=[
                "easy",
                "normal",
                "hard",
            ],
        )
        self.prompt_difficulty_combobox.grid(
            row=2, column=0, sticky="we", padx=5, pady=2
        )

        self.build_prompt_button = ttk.Button(
            generation_prompts_frame,
            text="Build Prompt",
            command=self.build_and_set_prompt,
        )
        self.build_prompt_button.grid(row=3, column=0, sticky="e", padx=5, pady=2)

        self.prompt_textbox = tk.Text(
            generation_prompts_frame,
            width=50,
            height=5,
            wrap="word",
        )
        self.prompt_textbox.grid(row=4, column=0, sticky="nswe", padx=5)
        self.prompt_textbox.insert("1.0", default_prompt)

    def get_exercise_generation_prompt(self) -> str:
        return self.prompt_textbox.get("1.0", tk.END).strip()

    def set_exercise_generation_prompt(self, prompt: str) -> None:
        self.prompt_textbox.delete("1.0", tk.END)
        self.prompt_textbox.insert("1.0", prompt)

    def get_prompt_register(self) -> str:
        return self.prompt_register_combobox.get_choice()

    def get_prompt_objective(self) -> str:
        return self.prompt_objective_combobox.get_choice()

    def get_prompt_difficulty(self) -> str:
        return self.prompt_difficulty_combobox.get_choice()

    def build_and_set_prompt(self) -> None:
        difficulty = self.get_prompt_difficulty()
        context_complexity = "simple" if difficulty in ["easy", "normal"] else "complex"
        num_objectives = 2 if difficulty == "easy" else 3

        prompt = "Generate a new email exercise with the following specifications:"
        prompt += f"\n- Difficulty: {difficulty} ({context_complexity} context with {num_objectives} specific objectives)."
        prompt += f"\n- Register: {self.get_prompt_register()}."
        prompt += f"\n- General objective: {self.get_prompt_objective()}."

        self.set_exercise_generation_prompt(prompt)

    def get_exercise_tag(self) -> str:
        return self.exercise_tag_entry.get()

    def get_solution_tag(self) -> str:
        return self.solution_tag_entry.get()


class SettingsFrame(ttk.Frame):
    """Container frame grouping API configuration and prompt settings."""

    def __init__(
        self,
        parent: tk.Misc,
        model_options: list[str],
        default_prompt: str = "Generate a new email exercise.",
    ) -> None:
        super().__init__(parent)
        self.columnconfigure(index=0, weight=1)
        self.rowconfigure(index=1, weight=1)

        self.api_config_frame = ApiConfigFrame(
            parent=self,
            model_options=model_options,
        )
        self.api_config_frame.grid(row=0, column=0, sticky="we", padx=10, pady=(5, 10))

        self.prompts_config_frame = PromptsConfigFrame(
            parent=self,
            default_prompt=default_prompt,
        )
        self.prompts_config_frame.grid(
            row=1, column=0, sticky="nsew", padx=10, pady=(10, 5)
        )

    def get_api_key(self) -> str:
        """Returns the current API key."""
        return self.api_config_frame.get_api_key()

    def get_model(self) -> str:
        """Returns the currently selected model."""
        return self.api_config_frame.get_model()

    def get_exercise_generation_prompt(self) -> str:
        """Returns the prompt template for exercise generation."""
        return self.prompts_config_frame.get_exercise_generation_prompt()

    def get_exercise_tag(self) -> str:
        """Returns the tag delimiter for the exercise text."""
        return self.prompts_config_frame.get_exercise_tag()

    def get_solution_tag(self) -> str:
        """Returns the tag delimiter for the solution text."""
        return self.prompts_config_frame.get_solution_tag()


class EmailResponseFrame(ttk.Frame):
    """Custom widget where the user writes the email response."""

    def __init__(self, parent: tk.Misc) -> None:
        super().__init__(parent)

        self.rowconfigure(3, weight=1)
        self.columnconfigure(0, weight=1)

        self.timer_frame = TimerFrame(parent=self, duration=420)
        self.timer_frame.grid(row=0, column=0, sticky="e", padx=5, pady=5)

        self.recipient_entry = LabeledEntry(parent=self, label_text="To", label_width=6)
        self.recipient_entry.grid(row=1, column=0, sticky="we", padx=5, pady=5)

        self.subject_entry = LabeledEntry(
            parent=self, label_text="Subject", label_width=6
        )
        self.subject_entry.grid(row=2, column=0, sticky="we", padx=5, pady=5)

        self.text_box = tk.Text(
            self, font=("Arial", 14), width=50, wrap="word", padx=5, pady=5
        )
        self.text_box.grid(row=3, column=0, sticky="nsew", padx=5, pady=5)

        self.clear_button = ttk.Button(self, text="clear", command=self.clear)
        self.clear_button.grid(row=4, column=0, sticky="e", padx=5, pady=5)

    def get_response(self) -> dict[str, str]:
        """Returns a dictionary with the recipient, subject and body of the current solution."""
        return {
            "recipient": self.recipient_entry.get(),
            "subject": self.subject_entry.get(),
            "body": self.text_box.get("1.0", tk.END).strip(),
        }

    def clear(self) -> None:
        """Clears all input fields in the response frame."""
        self.recipient_entry.clear()
        self.subject_entry.clear()
        self.text_box.delete("1.0", tk.END)


class EmailPracticeApp(tk.Tk):
    def __init__(
        self,
        model_options: list[str],
        assistant_system_prompt: str,
        email_generator_system_prompt: str,
        email_generation_format: dict,
        default_prompt: str = "Generate a new email exercise.",
    ) -> None:
        super().__init__()
        self.title("TOEFL Practice: Writing an e-mail")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        hpane = ttk.PanedWindow(self, orient="horizontal")
        hpane.grid(row=0, column=0, sticky="nsew")

        # Left pane = settings and exercise instructions
        self.config_and_exercise_notebook = ttk.Notebook(hpane)
        self.config_and_exercise_notebook.grid(row=0, column=0, sticky="nsew")

        self.settings_frame = SettingsFrame(
            parent=self.config_and_exercise_notebook,
            model_options=model_options,
            default_prompt=default_prompt,
        )
        self.settings_frame.api_config_frame.set_api_button_command(
            self.on_save_api_press
        )
        self.config_and_exercise_notebook.add(self.settings_frame, text="settings")

        self.instructions_frame = InstructionsFrame(
            parent=self.config_and_exercise_notebook
        )
        self.config_and_exercise_notebook.add(self.instructions_frame, text="exercise")

        hpane.add(self.config_and_exercise_notebook, weight=1)

        # Central pane = email writing
        self.email_response_frame = EmailResponseFrame(parent=hpane)
        hpane.add(self.email_response_frame, weight=1)

        # Right pane = assistant chat
        self.assistant_chat_frame = LLMChatFrame(parent=hpane)
        self.assistant_chat_frame.set_send_command(self.on_send_press)
        hpane.add(self.assistant_chat_frame)

        # API related
        self.api_client = OpenRouterClient(api_key="")
        self.chat_session = LLMChatSession(
            api_client=self.api_client,
            model=self.settings_frame.get_model(),
            system_prompt=assistant_system_prompt,
        )
        self.exercise_generator = EmailExerciseGenerator(
            model=self.settings_frame.get_model(),
            system_prompt=email_generator_system_prompt,
            response_format=email_generation_format,
            api_client=self.api_client,
        )

        self.instructions_frame.set_generate_command(self.handle_generate_exercise)

        # Prompts and formats
        self.assistant_system_prompt = assistant_system_prompt
        self.email_generator_system_prompt = email_generator_system_prompt
        self.email_generation_format = email_generation_format

    def on_save_api_press(self) -> None:
        """Saves the API key from the settings frame into the api_client."""
        self.api_client.set_api_key(self.settings_frame.get_api_key())

    def handle_generate_exercise(self) -> None:
        """Generates a new exercise and updates the InstructionsFrame."""

        # Sync the currently selected model before calling the API
        self.exercise_generator.model = self.settings_frame.get_model()

        exercise_prompt = self.settings_frame.get_exercise_generation_prompt()
        exercise = str(self.exercise_generator.generate(user_prompt=exercise_prompt))

        self.instructions_frame.set_exercise(exercise)
        self.config_and_exercise_notebook.select(self.instructions_frame)

    def on_send_press(self) -> None:
        """Handles sending user chat messages and processing placeholders."""
        raw_message = self.assistant_chat_frame.get_input_text().strip()
        if not raw_message:
            return

        # Visual updates in UI
        self.assistant_chat_frame.clear_input()
        self.assistant_chat_frame.add_user_message(raw_message)

        # Sync model selection
        self.chat_session.model = self.settings_frame.get_model()

        # Build solution string (To, Subject, Body)
        response_data = self.email_response_frame.get_response()
        formatted_solution = (
            f"To: {response_data['recipient']}\n"
            f"Subject: {response_data['subject']}\n\n"
            f"{response_data['body']}"
        ).strip()

        # Process placeholders
        processed_message = raw_message.replace(
            self.settings_frame.get_exercise_tag(),
            self.instructions_frame.get_exercise().strip(),
        )
        processed_message = processed_message.replace(
            self.settings_frame.get_solution_tag(),
            formatted_solution,
        )

        assistant_response = self.chat_session.send_message(processed_message)
        self.assistant_chat_frame.add_assistant_message(assistant_response)


def main() -> None:
    model_options = [
        "google/gemini-3.7-flash",
        "anthropic/claude-sonnet-4.6",
        "google/gemini-2.5-flash",
        "openai/gpt-5.6-luna",
    ]
    email_practice_app = EmailPracticeApp(
        model_options=model_options,
        assistant_system_prompt=EMAIL_ASSISTANT_SYSTEM_PROMPT,
        email_generator_system_prompt=EMAIL_GENERATOR_SYSTEM_PROMPT,
        email_generation_format=EMAIL_GENERATION_FORMAT,
    )
    email_practice_app.mainloop()


if __name__ == "__main__":
    main()
