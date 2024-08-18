import shutil

import numpy

from src.triangle import Triangle


def _get_screen_size():
    terminal_size = shutil.get_terminal_size()
    height, width = terminal_size.lines, terminal_size.columns

    return width // 2, height


class Screen:
    RESET: str = "\033[m"

    def __init__(self):
        self._size: tuple[int, int] = _get_screen_size()
        self._aspect_ratio: float = self._size[0] / self._size[1]
        self._frame_buffer: numpy.ndarray = numpy.full(
            shape=(self._size[1], self._size[0] * 2), dtype=object, fill_value=" "
        )

        print(self._frame_buffer.shape, self._size)

    def _write_frame_buffer(self, position: tuple[int, int], pixel: tuple[str, str] = ("█", "█")):
        self._frame_buffer[position[1], position[0] * 2] = pixel[0]
        self._frame_buffer[position[1], position[0] * 2 + 1] = pixel[1]

    def _project(self, vertex: numpy.ndarray) -> numpy.ndarray:
        if vertex[2] != 0.0:
            x_proj: float = vertex[0] / -vertex[2]
            y_proj: float = vertex[1] / -vertex[2] * self._aspect_ratio

        else:
            x_proj: float = 0.0
            y_proj: float = 0.0

        x_proj_remap: float = (x_proj + 1) / 2
        y_proj_remap: float = (y_proj + 1) / 2

        return numpy.array([x_proj_remap * self._size[0], y_proj_remap * self._size[1]], dtype=int)

    def clear(self):
        self._frame_buffer[self._frame_buffer != " "] = " "

    def add_ui(self, stats: dict):
        # Add frame
        for index, string in enumerate("╭" + "─" * (self._size[0] * 2 - 2) + "╮"):
            self._frame_buffer[0, index] = string

        for viewport_y in range(1, self._size[1] - 1):
            self._write_frame_buffer((0, viewport_y), (self.RESET + "│", " "))
            self._write_frame_buffer((self._size[0] - 1, viewport_y), (self.RESET + " ", "│"))

        for index, string in enumerate("╰" + "─" * (self._size[0] * 2 - 2) + "╯"):
            self._frame_buffer[-1, index] = string

        # Add stats
        longest_key: int = max(map(len, stats.keys()))
        longest_value: int = max(map(lambda value: len(str(value[0])), stats.values()))
        longest_unit: int = max(map(lambda unit: len(unit[1]), stats.values()))
        ui_widget_width: int = longest_key + longest_value + longest_unit + 2
        self._frame_buffer[0, ui_widget_width + 3] = "┬"

        for index, (stat_name, (stat_value, stat_unit)) in enumerate(stats.items()):
            stat: str = (
                f"{stat_name.ljust(longest_key)} {str(stat_value).rjust(longest_value)} {stat_unit.ljust(longest_unit)}"
            )

            self.draw_text(stat, (index + 1, 2))

            self._frame_buffer[index + 1, ui_widget_width + 2] = self.RESET + " "
            self._frame_buffer[index + 1, ui_widget_width + 3] = "│"
            self._frame_buffer[index + 1, ui_widget_width + 4] = " "

        for index, string in enumerate("├" + "─" * (ui_widget_width + 2) + "╯ "):
            self._frame_buffer[len(stats) + 1, index] = string

    def print_frame(self):
        stdout_buffer: str = "\033[H\033[?25l" + "".join(map(lambda line: "".join(line), self._frame_buffer))

        print(stdout_buffer, end="", flush=True)

    def draw_vertex(self, vertex: numpy.ndarray):
        x, y = self._project(vertex)
        self._write_frame_buffer((x, y))

    def draw_text(self, text: str, position: tuple[int, int]):
        for index, character in enumerate(text):
            self._frame_buffer[position[0], position[1] + index] = character

    def _get_line_pixels(self, start: numpy.ndarray, stop: numpy.ndarray) -> list[tuple[int, int]]:
        pixel_coordinates: list[tuple[int, int]] = []
        start: numpy.ndarray = self._project(start)
        stop: numpy.ndarray = self._project(stop)
        signX: int = -1 if start[0] > stop[0] else 1
        signY: int = -1 if start[1] > stop[1] else 1
        difference: numpy.ndarray = numpy.abs(stop - start)
        m: float = float(difference[1] / difference[0] if difference[0] > 0 else difference[1] / 0.00001)

        if m <= 1:
            for i in range(difference[0]):
                x: int = int(numpy.ceil(start[0] + i * signX))
                y: int = int(numpy.ceil(start[1] + i * m * signY))
                pixel_coordinates.append((x, y))

        else:
            for i in range(difference[1]):
                x: int = int(numpy.ceil(start[0] + i / m * signX))
                y: int = int(numpy.ceil(start[1] + i * signY))
                pixel_coordinates.append((x, y))

        return pixel_coordinates

    def draw_line(self, start: numpy.ndarray, stop: numpy.ndarray):
        for pixel_coordinate in self._get_line_pixels(start, stop):
            self._write_frame_buffer(pixel_coordinate)

    def draw_triangle(self, triangle: Triangle):
        for index, vertex in enumerate(triangle.vertices):
            start: numpy.ndarray = self._project(vertex)
            stop: numpy.ndarray = self._project(triangle[(index + 1) % 3])
            self.draw_line(numpy.asarray(start), numpy.asarray(stop))

    def draw_quad(self, vertices: list[numpy.ndarray]):
        self.draw_line(start=vertices[0], stop=vertices[1])
        self.draw_line(start=vertices[1], stop=vertices[3])
        self.draw_line(start=vertices[3], stop=vertices[2])
        self.draw_line(start=vertices[2], stop=vertices[0])
