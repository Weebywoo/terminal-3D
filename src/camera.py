import os

import numpy

from src.canvas import Canvas
from src.geometry_manipulation import translate_vertex_around_camera
from src.mesh import Mesh


def _get_screen_size():
    terminal_size = os.get_terminal_size()
    height, width = terminal_size.lines, terminal_size.columns

    return width // 2, height


class Camera:
    THETA: float = 0.00001

    def __init__(self, position: numpy.ndarray, orientation: numpy.ndarray):
        self.size: tuple[int, int] = _get_screen_size()
        self.aspect_ratio: float = self.size[0] / self.size[1]
        self._position: numpy.ndarray = position
        self._orientation: numpy.ndarray = orientation
        self._canvas: Canvas = Canvas(self.size, self._projector)

    def _projector(self, vertex: numpy.ndarray) -> numpy.ndarray:
        # rotate vertex around camera in -orientation direction

        # translated_vertex = vertex - self._position
        translated_vertex = translate_vertex_around_camera(vertex, self._position, self._orientation)
        divisor: float = -(translated_vertex[2] + self.THETA)
        x_proj: float = translated_vertex[0] / divisor
        y_proj: float = translated_vertex[1] / divisor * self.aspect_ratio
        x_proj_remap: float = (x_proj + 1) / 2
        y_proj_remap: float = (y_proj + 1) / 2

        return numpy.array([x_proj_remap * self.size[0], self.size[1] - y_proj_remap * self.size[1]], dtype=int)

    def render(
        self, meshes: list[Mesh], frame: int, last_frame_time: float, last_render_time: float, target_frame_time: float
    ):
        self._canvas.clear()

        for mesh in meshes:
            # self._canvas.draw_mesh(mesh)
            for triangle in mesh:
                self._canvas.draw_triangle(triangle)

        self._canvas.add_frame(frame, last_frame_time, last_render_time, target_frame_time)
        self.print()

    def rotate(self, delta: tuple[float, float, float]):
        self._orientation[0] += delta[0]
        self._orientation[1] += delta[1]
        self._orientation[2] += delta[2]

    def move(self, delta: tuple[float, float, float]):
        self._position[0] += delta[0]
        self._position[1] += delta[1]
        self._position[2] += delta[2]

    def print(self):
        stdout_buffer: str = "\033[H\033[?25l" + "".join(map(lambda line: "".join(line), self._canvas.frame_buffer))

        print(stdout_buffer, end="", flush=True)
