import tkinter as tk
from tkinter import ttk, messagebox

import time

class Timer:
    IDLE = "idle"
    RUNNING = "running"
    PAUSED = "paused"
    FINISHED = "finished"

    def __init__(self, duration: int = 420) -> None:
        """Initializes a new timer with a given duration in seconds."""
        self.duration = duration
        self.time_left = duration
        self.state = Timer.IDLE

    def start(self) -> None:
        """Starts or resumes the timer if there is remaining time and not finished."""
        if self.time_left > 0 and self.state != Timer.FINISHED:
            self.state = Timer.RUNNING

    def pause(self) -> None:
        """Pauses the timer if it is currently running."""
        if self.state == Timer.RUNNING:
            self.state = Timer.PAUSED

    def update(self, elapsed: int) -> None:
        """Updates the remaining time and state if the timer is running."""
        if self.state != Timer.RUNNING:
            return

        self.time_left = max(self.time_left - elapsed, 0)
        if self.time_left == 0:
            self.state = Timer.FINISHED

    def reset(self) -> None:
        """Resets the timer back to its initial idle state and restores remaining time."""
        self.time_left = self.duration
        self.state = Timer.IDLE

    def set_duration(self, duration: int) -> None:
        """Sets a new duration and resets the timer to idle state."""
        self.duration = duration
        self.reset()


class TimerFrame(ttk.Frame):
    def __init__(self, parent: tk.Misc, duration: int = 420) -> None:
        super().__init__(parent)
        self.columnconfigure(index=0, weight=1)

        duration = max(duration, 0)
        duration = min(duration, 30 * 60)
        self.timer = Timer(duration=duration)
        self._after_id = None

        self.time_label = ttk.Label(
            self,
            text=self.convert_seconds_to_timer_string(self.timer.duration),
        )
        self.time_label.grid(row=0, column=0, padx=2, pady=2)

        self.timer_button = ttk.Button(self, text="start", command=self.start)
        self.timer_button.grid(row=0, column=1, padx=2, pady=2)

    def convert_seconds_to_timer_string(self, seconds: int) -> str:
        return time.strftime("%M:%S", time.gmtime(seconds))

    def start(self) -> None:
        self.timer.start()
        self.timer_button.configure(
            text="reset",
            command=self.reset,
        )
        self._after_id = self.after(1000, self.update_clock)

    def reset(self) -> None:
        if self._after_id is not None:
            self.after_cancel(self._after_id)
            self._after_id = None

        self.timer.reset()
        self.time_label.configure(
            text=self.convert_seconds_to_timer_string(self.timer.duration),
        )
        self.timer_button.configure(
            text="start",
            command=self.start,
        )

    def update_clock(self) -> None:
        self.timer.update(elapsed=1)
        self.time_label.configure(
            text=self.convert_seconds_to_timer_string(self.timer.time_left)
        )

        if self.timer.state == Timer.RUNNING:
            self._after_id = self.after(ms=1000, func=self.update_clock)
        elif self.timer.state == Timer.FINISHED:
            self._after_id = None
            self.time_label.config(
                text=self.convert_seconds_to_timer_string(self.timer.time_left)
            )
            self.update_idletasks()
            messagebox.showinfo(title="Message from Timer", message="Time's up!")




if __name__ == "__main__":
    root = tk.Tk()
    root.columnconfigure(index=0, weight=1)

    timer_frame = TimerFrame(root, duration=10)
    timer_frame.grid(row=0, column=0, sticky="we")

    root.mainloop()

