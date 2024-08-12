import shutil
import time

import numpy

from src.console import add_ui, print_frame, add_render
from src.viewport import get_marchingcubes_viewport


def main():
    terminal_size = shutil.get_terminal_size()
    height, width = terminal_size.lines, terminal_size.columns

    position: numpy.ndarray = numpy.array([0, 0, 0], dtype=int)
    voxel_storage: dict[tuple, list] = {}
    frame_times: list[float] = []
    last_avg_frame_time: int = 0
    last_avg_fps: int = 0

    frame_buffer: numpy.ndarray = numpy.full(shape=(height, width), dtype=object, fill_value=" ")

    for y in range(500):
        start_time: float = time.time()
        viewport: numpy.ndarray = get_marchingcubes_viewport(position, (height, width // 2), voxel_storage)
        stats: dict[str, tuple[int, str]] = {
            "FPS": (int(round(last_avg_fps)), "fps"),
            "Frame time": (int(round(last_avg_frame_time)), "ms"),
        }

        add_render(frame_buffer, viewport)
        add_ui(frame_buffer, height, width, stats)
        print_frame(frame_buffer)

        position[1] = y

        end_time: float = time.time()

        if len(frame_times) >= 5:
            frame_times.pop(0)

        frame_times.append(end_time - start_time)

        last_avg_frame_time: float = (sum(frame_times) / len(frame_times)) * 1000
        last_avg_fps: float = 1 / (last_avg_frame_time / 1000)

    # plt.show()


if __name__ == "__main__":
    main()
