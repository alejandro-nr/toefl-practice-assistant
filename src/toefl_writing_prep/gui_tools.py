import tkinter as tk
from collections.abc import Callable
from tkinter import ttk


class LabeledEntry(ttk.Frame):
    def __init__(
        self,
        parent: tk.Misc,
        label_text: str,
        label_width: int,
        initial_entry_text: str | None = None,
    ) -> None:
        """A custom widget pairing a label with a text entry in a single row."""
        super().__init__(parent)
        self.columnconfigure(1, weight=1)

        self.label = ttk.Label(self, text=label_text, width=label_width, anchor="w")
        self.label.grid(row=0, column=0, sticky="w")

        self.entry = ttk.Entry(self)
        self.entry.grid(row=0, column=1, sticky="ew")

        if initial_entry_text is not None:
            self.entry.insert(0, initial_entry_text)

    def get(self) -> str:
        """Returns the current text in the entry."""
        return self.entry.get()


class LabeledCombobox(ttk.Frame):
    def __init__(
        self,
        parent: tk.Misc,
        text: str,
        label_width: int,
        combobox_width: int,
        choices: list[str] | None = None,
    ) -> None:
        """A custom widget pairing a label with a combobox in a single row."""
        super().__init__(parent)
        self.rowconfigure(index=0, weight=1)
        self.columnconfigure(index=1, weight=1)

        self.label = ttk.Label(self, text=text, width=label_width, anchor="w")
        self.label.grid(row=0, column=0, sticky="w")

        if choices is None:
            choices = []
        self.current_value = tk.StringVar()
        self.combobox = ttk.Combobox(
            self,
            textvariable=self.current_value,
            width=combobox_width,
            values=choices,
            state="readonly",
        )
        if choices:
            self.combobox.current(newindex=0)
        self.combobox.grid(row=0, column=1, sticky="we")

    def get_choice(self) -> str:
        """Returns the current value as a string."""
        return self.current_value.get()

    def bind_combobox(self, callback: Callable[..., object]) -> None:
        """Binds the value changes of the combobox to a callback function."""
        self.combobox.bind("<<ComboboxSelected>>", callback)


if __name__ == "__main__":
    root = tk.Tk()
    root.columnconfigure(index=0, weight=1)

    labeled_entry = LabeledEntry(
        parent=root,
        label_text="Label text",
        label_width=20,
        initial_entry_text="Initial text...",
    )
    labeled_entry.grid(row=0, column=0, sticky="nwe")

    labeled_combobox = LabeledCombobox(
        parent=root,
        text="Combo-box label",
        label_width=20,
        combobox_width=20,
        choices=[f"choice {i}" for i in range(1, 11)],
    )
    labeled_combobox.grid(row=1, column=0, sticky="nwe")

    root.mainloop()
