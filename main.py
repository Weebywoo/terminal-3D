import shutil
import time

import numpy

from src.console import print_viewport, print_frame
from src.viewport import get_marchingcubes_viewport


def main():
    terminal_size = shutil.get_terminal_size()
    width, height = terminal_size.columns, terminal_size.lines
    height -= 1

    position: numpy.ndarray = numpy.array([0, 0, 0], dtype=int)
    size: tuple[int, int] = (height - 2, (width - 4) // 2)
    voxel_storage: dict[tuple, list] = {}
    frame_times: list[float] = []

    print_frame(height, width)

    for y in range(500):
        start_time: float = time.time()
        viewport: numpy.ndarray = get_marchingcubes_viewport(position, size, voxel_storage)
        print_viewport(viewport)

        position[1] = y  # handle_controls()
        end_time: float = time.time()

        if len(frame_times) >= 5:
            frame_times.pop(0)

        frame_times.append(end_time - start_time)

        cursor_position: str = f"\033[{height + 1};{1}H"

        avg_frame_time: float = (sum(frame_times) / len(frame_times)) * 1000
        fps: float = round(1 / (avg_frame_time / 1000), 2)

        frame_time_formated: str = str(int(avg_frame_time)).rjust(4)
        fps_formated: str = str(fps).rjust(5)

        print(cursor_position, frame_time_formated + "ms", fps_formated + "fps", end="")

    # plt.show()


if __name__ == "__main__":
    main()
