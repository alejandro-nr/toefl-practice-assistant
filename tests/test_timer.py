from toefl_practice_assistant.core.timer import Timer


def test_initialization():
    assert Timer.RUNNING == "running"
    assert Timer.PAUSED == "paused"
    assert Timer.IDLE == "idle"
    assert Timer.FINISHED == "finished"

    duration = 420
    timer = Timer(duration=duration)

    assert timer.duration == duration
    assert timer.time_left == duration
    assert timer.state == Timer.IDLE


class TestStart:
    def test_start_from_new_timer(self) -> None:
        timer = Timer(duration=10)
        timer.start()
        assert timer.state == Timer.RUNNING

    def test_does_nothing_if_duration_is_zero(self) -> None:
        timer = Timer(duration=0)
        timer.start()
        assert timer.state == Timer.IDLE

    def test_does_not_start_if_state_is_finished(self) -> None:
        timer = Timer(duration=3)
        timer.start()
        timer.update(elapsed=3)
        timer.start()
        assert timer.state == Timer.FINISHED

    def test_resume_from_paused_state(self) -> None:
        timer = Timer(duration=10)
        timer.start()
        timer.update(elapsed=3)
        timer.pause()

        timer.start()
        assert timer.state == Timer.RUNNING
        assert timer.time_left == 7


class TestUpdate:
    def test_does_nothing_when_not_running(self) -> None:
        timer = Timer(duration=3)
        timer.update(elapsed=2)

        assert timer.duration == 3
        assert timer.time_left == 3

    def test_decrements_time_left_when_running(self) -> None:
        timer = Timer(duration=3)
        timer.start()
        timer.update(elapsed=2)

        assert timer.duration == 3
        assert timer.time_left == 1

    def test_changes_state_to_finished_when_time_left_reaches_zero(self) -> None:
        timer = Timer(duration=3)
        timer.start()
        timer.update(elapsed=3)

        assert timer.duration == 3
        assert timer.time_left == 0
        assert timer.state == Timer.FINISHED

    def test_clamps_time_left_to_zero_without_negative_values(self) -> None:
        timer = Timer(duration=1)
        timer.start()
        timer.update(elapsed=2)

        assert timer.time_left == 0
        assert timer.state == Timer.FINISHED


class TestPause:
    def test_does_nothing_if_state_is_idle(self) -> None:
        timer = Timer(duration=10)
        timer.pause()

        assert timer.state == Timer.IDLE

    def test_pauses_running_timer(self) -> None:
        timer = Timer(duration=10)
        timer.start()
        timer.update(elapsed=3)

        timer.pause()

        assert timer.state == Timer.PAUSED
        assert timer.time_left == 7
        assert timer.duration == 10

    def test_does_nothing_while_paused(self) -> None:
        timer = Timer(duration=10)
        timer.start()
        timer.update(elapsed=3)
        timer.pause()

        timer.update(elapsed=2)

        assert timer.state == Timer.PAUSED
        assert timer.time_left == 7
        assert timer.duration == 10


class TestReset:
    def test_reset_from_idle_state(self) -> None:
        timer = Timer(duration=3)
        timer.reset()

        assert timer.duration == 3
        assert timer.time_left == 3
        assert timer.state == Timer.IDLE

    def test_reset_from_running_state(self) -> None:
        timer = Timer(duration=3)
        timer.start()
        timer.update(elapsed=1)

        timer.reset()

        assert timer.duration == 3
        assert timer.time_left == 3
        assert timer.state == Timer.IDLE

    def test_reset_from_paused_state(self) -> None:
        timer = Timer(duration=3)
        timer.start()
        timer.update(elapsed=1)
        timer.pause()

        timer.reset()

        assert timer.duration == 3
        assert timer.time_left == 3
        assert timer.state == Timer.IDLE

    def test_reset_from_finished_state(self) -> None:
        timer = Timer(duration=3)
        timer.start()
        timer.update(elapsed=3)

        timer.reset()

        assert timer.duration == 3
        assert timer.time_left == 3
        assert timer.state == Timer.IDLE


class TestSetDuration:
    def test_set_duration_in_idle_state(self) -> None:
        timer = Timer(duration=10)
        timer.set_duration(20)

        assert timer.duration == 20
        assert timer.time_left == 20
        assert timer.state == Timer.IDLE
