import time
from typing import Any


class Timer:
    def __init__(self, function):
        self._function = function
        self._frame_times: list[float] = []

    def __call__(self, *args, **kwargs) -> Any:
        start_time: float = time.time()

        if len(self._frame_times) == 0 or sum(self._frame_times) == 0:
            moving_average_frame_duration = 1e-10

        else:
            moving_average_frame_duration = sum(self._frame_times) / len(self._frame_times)

        stats: dict[str, tuple[int, str]] = {
            "FPS": (int(round(1 / moving_average_frame_duration)), "fps"),
            "Frame time": (int(round(moving_average_frame_duration)), "ms"),
        }

        result: Any = self._function(*args, **kwargs, stats=stats)

        end_time: float = time.time()

        if len(self._frame_times) >= 15 * 60:
            self._frame_times.pop(0)

        self._frame_times.append(end_time - start_time)

        return result
