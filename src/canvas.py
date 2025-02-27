import numpy

from src import terminal_size


class Canvas:
    def __init__(self) -> None:
        self._frame_buffer: numpy.ndarray = numpy.full(
            shape=(terminal_size.height, terminal_size.width), dtype=bool, fill_value=False
        )

    def draw_pixel(self, pixel: tuple[int, int]) -> None:
        x, y = pixel[0], (terminal_size.height - 1) - pixel[1]

        if 0 <= x < terminal_size.width and 0 <= y < terminal_size.height:
            self._frame_buffer[y, x] = True

    def clear(self) -> None:
        self._frame_buffer[self._frame_buffer == True] = False

    def draw(self):
        stdout_buffer: str = "\033[H\033[?25l"

        for y in range(0, terminal_size.height, 2):
            for x in range(terminal_size.width):
                match (bool(self._frame_buffer[y, x]), bool(self._frame_buffer[y + 1, x])):
                    case (True, False):
                        stdout_buffer += "▀"

                    case (True, True):
                        stdout_buffer += "█"

                    case (False, True):
                        stdout_buffer += "▄"

                    case (False, False):
                        stdout_buffer += " "

        print(stdout_buffer, end="", flush=True)

    # def draw_line(self, start: tuple[int, int], end: tuple[int, int]) -> None:
    #     if start[0] > end[0]:
    #         end, start = start, end
    #
    #     dx: int = end[0] - start[0]
    #     dy: int = end[1] - start[1]
    #
    #     if dx == 0:
    #         dx = 1
    #
    #     m: float = dy / dx
    #
    #     for x in range(start[0], end[0]):
    #         y: float = m * (x - start[0]) + start[1]
    #
    #         self.draw_pixel((x, int(y)))

    def draw_line(self, start: tuple[int, int], end: tuple[int, int]):
        dx: int = end[0] - start[0]
        dy: int = end[1] - start[1]

        if dx == 0 or dy == 0:
            return

        step: int = max(abs(dx), abs(dy))
        step_x: float = dx / step
        step_y: float = dy / step

        for offset in range(step + 1):
            self.draw_pixel((int(round(start[0] + offset * step_x)), int(round(start[1] + offset * step_y))))
