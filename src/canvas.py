import numpy

from src.mesh import Mesh


def cross(a: numpy.ndarray, b: numpy.ndarray) -> numpy.ndarray:
    return numpy.cross(a, b)


def orientation(a, b, c):
    if cross(b - a, c - a) > 0:
        return 1
    else:
        return -1


def _check_pixel_in_triangle(
    pixel: numpy.ndarray, vertex_one: numpy.ndarray, vertex_two: numpy.ndarray, vertex_three: numpy.ndarray
) -> bool:
    turns = (
        orientation(vertex_one, vertex_two, pixel)
        + orientation(vertex_two, vertex_three, pixel)
        + orientation(vertex_three, vertex_one, pixel)
    )

    return turns == 3


class Canvas:
    RESET: str = "\033[m"
    THETA: float = 0.00001

    def __init__(self, size_accessor, projector):
        self._size_accessor = size_accessor
        self._projector = projector
        self.frame_buffer: numpy.ndarray = numpy.full(
            shape=(self._size_accessor[1], self._size_accessor[0] * 2), dtype=object, fill_value=" "
        )

    def set_pixel(self, position: tuple[int, int], pixel: tuple[str, str] = ("█", "█")):
        width, height = self._size_accessor

        if 0 <= position[0] < width and 0 <= position[1] < height:
            self.frame_buffer[position[1], position[0] * 2] = pixel[0]
            self.frame_buffer[position[1], position[0] * 2 + 1] = pixel[1]

    def clear(self):
        self.frame_buffer[self.frame_buffer != " "] = " "

    def add_frame(self, frame: int, last_frame_time: float, last_render_time: float, target_frame_time: float):
        # Add frame
        for index, string in enumerate("╭" + "─" * (self._size_accessor[0] * 2 - 2) + "╮"):
            self.frame_buffer[0, index] = string

        for viewport_y in range(1, self._size_accessor[1] - 1):
            self.set_pixel((0, viewport_y), (self.RESET + "│", " "))
            self.set_pixel((self._size_accessor[0] - 1, viewport_y), (self.RESET + " ", "│"))

        for index, string in enumerate("╰" + "─" * (self._size_accessor[0] * 2 - 2) + "╯"):
            self.frame_buffer[-1, index] = string

        # Add stats
        frames_per_second: int = int(round(1 / last_frame_time)) if last_frame_time != 0.0 else 0
        milliseconds_render_time: int = int(round(last_render_time * 1000))
        milliseconds_per_frame: int = int(round(last_frame_time * 1000))
        milliseconds_target_frame_time: int = int(round(target_frame_time * 1000))
        self.frame_buffer[0, 23] = "┬"

        self.draw_text(f"Frame       {frame:>4}", (2, 1))
        self.draw_text(f"FPS         {frames_per_second:>4} fps", (2, 2))
        self.draw_text(f"Render time {milliseconds_render_time:>4} ms", (2, 3))
        self.draw_text(f"Frame time  {milliseconds_per_frame:>4} ms", (2, 4))
        self.draw_text(f"Target time {milliseconds_target_frame_time:>4} ms", (2, 5))

        self.set_pixel((11, 1), (self.RESET + " ", "│"))
        self.set_pixel((11, 2), (self.RESET + " ", "│"))
        self.set_pixel((11, 3), (self.RESET + " ", "│"))
        self.set_pixel((11, 4), (self.RESET + " ", "│"))
        self.set_pixel((11, 5), (self.RESET + " ", "│"))

        for index, string in enumerate("├" + "─" * 22 + "╯ "):
            self.frame_buffer[6, index] = string

    def draw_vertex(self, vertex: numpy.ndarray):
        canvas_2d_coordinates: numpy.ndarray | None = self._projector(vertex)

        if canvas_2d_coordinates is None:
            return

        self.set_pixel(canvas_2d_coordinates)

    def draw_text(self, text: str, position: tuple[int, int]):
        for index, character in enumerate(text):
            self.frame_buffer[position[1], position[0] + index] = character

    def _get_line_pixels(self, start: numpy.ndarray, stop: numpy.ndarray) -> list[tuple[int, int]] | None:
        pixel_coordinates: list[tuple[int, int]] = []
        start: numpy.ndarray = self._projector(start)
        stop: numpy.ndarray = self._projector(stop)

        if start is None or stop is None:
            return

        signX: int = -1 if start[0] > stop[0] else 1
        signY: int = -1 if start[1] > stop[1] else 1
        difference: numpy.ndarray = numpy.abs(stop - start)
        m: float = float(difference[1] / (difference[0] + self.THETA))

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
        canvas_2d_coordinates: list[tuple[int, int]] | None = self._get_line_pixels(start, stop)

        if canvas_2d_coordinates is None:
            return

        for pixel_coordinate in canvas_2d_coordinates:
            self.set_pixel(pixel_coordinate)

    def draw_triangle(self, triangle: tuple[numpy.ndarray, numpy.ndarray, numpy.ndarray]):
        # vertex_one: numpy.ndarray = self._projector(triangle.vertices[0])
        # vertex_two: numpy.ndarray = self._projector(triangle.vertices[1])
        # vertex_three: numpy.ndarray = self._projector(triangle.vertices[2])
        # triangle_bounding_box: tuple[numpy.ndarray, numpy.ndarray] = calculate_2d_bounding_box(
        #     [vertex_one, vertex_two, vertex_three]
        # )
        # start, stop = triangle_bounding_box
        #
        # for x in range(start[0], stop[0]):
        #     for y in range(start[1], stop[1]):
        #         if _check_pixel_in_triangle(numpy.array([x, y]), vertex_one, vertex_two, vertex_three):
        #             self.set_pixel((x, y))

        for index, vertex in enumerate(triangle):
            self.draw_line(vertex, triangle[(index + 1) % 3])

    def draw_mesh(self, mesh: Mesh):
        for triangle in mesh:
            self.draw_triangle(triangle)
