import tkinter as tk
from tkinter import ttk
from typing import Literal


class ConversationFrame(ttk.Frame):
    """Scrollable conversation container displaying chat messages as speech bubbles."""

    def __init__(self, parent: tk.Misc) -> None:
        super().__init__(parent)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.canvas = tk.Canvas(self, width=70, height=200, bg="white")
        self.canvas.grid(row=0, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.conversation_frame = ttk.Frame(self.canvas, relief="groove", borderwidth=1)
        self.conversation_frame.columnconfigure(0, weight=1)

        self.canvas_window = self.canvas.create_window(
            0, 0, window=self.conversation_frame, anchor="nw"
        )
        self.conversation_frame.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind("<Configure>", self.on_canvas_configure)

        self.canvas.bind("<Enter>", self.bind_mousewheel)
        self.canvas.bind("<Leave>", self.unbind_mousewheel)

    def update_scroll_region(self) -> None:
        """Recalculates the scroll region and window dimensions based on content."""
        self.conversation_frame.update_idletasks()
        reqheight = self.conversation_frame.winfo_reqheight()
        canvas_height = self.canvas.winfo_height()
        final_height = canvas_height if reqheight < canvas_height else reqheight
        self.canvas.itemconfig(self.canvas_window, height=final_height)
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_mousewheel(self, event: tk.Event) -> None:
        """Handles mouse wheel scrolling inside the canvas."""
        if event.delta > 0:
            self.canvas.yview_scroll(-1, "units")
        else:
            self.canvas.yview_scroll(1, "units")

    def on_frame_configure(self, event: tk.Event) -> None:
        """Updates scroll region when internal frame resizes."""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_canvas_configure(self, event: tk.Event) -> None:
        """Resizes internal window to match canvas width and height."""
        natural_height = self.conversation_frame.winfo_reqheight()
        final_height = event.height if natural_height < event.height else natural_height
        self.canvas.itemconfig(
            self.canvas_window, width=event.width, height=final_height
        )

    def bind_mousewheel(self, event: tk.Event) -> None:
        """Binds mouse wheel events when cursor enters canvas."""
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)

    def unbind_mousewheel(self, event: tk.Event) -> None:
        """Unbinds mouse wheel events when cursor leaves canvas."""
        self.canvas.unbind_all("<MouseWheel>")

    def add_message(self, text: str, side: Literal["left", "right"]) -> None:
        """Adds a message bubble aligned to the left or right."""
        row = self.conversation_frame.grid_size()[1]
        bubble = ttk.Label(
            self.conversation_frame,
            text=text,
            relief="ridge",
            borderwidth=1,
            wraplength=300,
            justify="left",
            padding=6,
        )
        if side == "right":
            bubble.grid(row=row, column=0, sticky="e", padx=(80, 5), pady=3)
        elif side == "left":
            bubble.grid(row=row, column=0, sticky="w", padx=(5, 80), pady=3)

        self.update_scroll_region()
        self.canvas.yview_moveto(1.0)


if __name__ == "__main__":
    root = tk.Tk()
    root.rowconfigure(index=0, weight=1)
    root.columnconfigure(index=0, weight=1)

    conversation_frame = ConversationFrame(root)
    conversation_frame.grid(row=0, column=0, sticky="nsew")

    conversation_frame.add_message(text="Hello, how are you", side="right")
    conversation_frame.add_message(text="Hello, how are you", side="left")
    conversation_frame.add_message(text="Hello, how are you", side="right")
    conversation_frame.add_message(text="Hello, how are you", side="left")
    conversation_frame.add_message(text="Hello, how are you", side="right")
    conversation_frame.add_message(text="Hello, how are you", side="left")
    conversation_frame.add_message(text="Hello, how are you", side="right")

    root.mainloop()
