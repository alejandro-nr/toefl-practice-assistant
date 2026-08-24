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
