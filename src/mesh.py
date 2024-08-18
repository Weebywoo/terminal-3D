import numpy
from scipy.spatial.transform import Rotation

from src.triangle import Triangle


def _calculate_boundary_box(vertices: list[numpy.ndarray]) -> tuple[numpy.ndarray, numpy.ndarray]:
    vertices: numpy.ndarray = numpy.asarray(vertices)
    z_axis: numpy.ndarray = vertices[0, :]
    y_axis: numpy.ndarray = vertices[1, :]
    x_axis: numpy.ndarray = vertices[2, :]
    z_min: numpy.ndarray = z_axis.min()
    z_max: numpy.ndarray = z_axis.max()
    y_min: numpy.ndarray = y_axis.min()
    y_max: numpy.ndarray = y_axis.max()
    x_min: numpy.ndarray = x_axis.min()
    x_max: numpy.ndarray = x_axis.max()

    return numpy.array([z_min, y_min, x_min]), numpy.array([z_max, y_max, x_max])


class Mesh:
    def __init__(self, vertices: list[numpy.ndarray], vertex_order: list[int] = None):
        self.vertices: list[numpy.ndarray] = vertices
        self.vertex_order: list[int] = vertex_order
        self.boundary_box: tuple[numpy.ndarray, numpy.ndarray] = _calculate_boundary_box(vertices)
        self.geometry_center: numpy.ndarray = numpy.sum(vertices, axis=0) / len(vertices)

    def rotate(self, radians: tuple[float, float, float]):
        self.rotate_x(radians[0])
        self.rotate_y(radians[1])
        self.rotate_z(radians[2])

    def rotate_x(self, radians: float):
        for index, vertex in enumerate(self.vertices):
            self.vertices[index] = self._rotate(vertex, radians, numpy.array([1, 0, 0]))

    def rotate_y(self, radians: float):
        for index, vertex in enumerate(self.vertices):
            self.vertices[index] = self._rotate(vertex, radians, numpy.array([0, 1, 0]))

    def rotate_z(self, radians: float):
        for index, vertex in enumerate(self.vertices):
            self.vertices[index] = self._rotate(vertex, radians, numpy.array([0, 0, 1]))

    def _rotate(self, vertex: numpy.ndarray, radians: float, axis: numpy.ndarray) -> numpy.ndarray:
        rotation_vector: numpy.ndarray = radians * axis
        rotation = Rotation.from_rotvec(rotation_vector)
        translated_vertex = vertex - self.geometry_center

        return rotation.apply(translated_vertex) + self.geometry_center

    @property
    def triangles(self) -> list[Triangle]:
        if self.vertex_order is None:
            return []

        return [
            Triangle(
                vertices=[
                    self.vertices[self.vertex_order[i]],
                    self.vertices[self.vertex_order[i + 1]],
                    self.vertices[self.vertex_order[i + 2]],
                ]
            )
            for i in range(0, len(self.vertex_order), 3)
        ]
