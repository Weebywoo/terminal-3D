import numpy

from src.geometry_manipulation import rotate_vertex, calculate_boundary_box


class Mesh(list):
    def __init__(self, vertices: list[numpy.ndarray], vertex_order: list[int] = None):
        super().__init__(
            [
                (vertices[vertex_order[i]], vertices[vertex_order[i + 1]], vertices[vertex_order[i + 2]])
                for i in range(0, len(vertex_order), 3)
            ]
        )
        self._vertices: list[numpy.ndarray] = vertices
        self.vertex_order: list[int] = vertex_order

        if len(vertices) == 1:
            self.boundary_box: tuple[numpy.ndarray, numpy.ndarray] = (vertices[0], vertices[0])

        else:
            self.boundary_box: tuple[numpy.ndarray, numpy.ndarray] = calculate_boundary_box(vertices)

        self.geometry_center: numpy.ndarray = numpy.sum(vertices, axis=0) / len(vertices)

    def rotate(self, radians: tuple[float, float, float]):
        self.rotate_x(radians[0])
        self.rotate_y(radians[1])
        self.rotate_z(radians[2])

    def rotate_x(self, radians: float):
        for index, vertex in enumerate(self._vertices):
            self._vertices[index] = rotate_vertex(vertex, radians, numpy.array([1, 0, 0]), self.geometry_center)

    def rotate_y(self, radians: float):
        for index, vertex in enumerate(self._vertices):
            self._vertices[index] = rotate_vertex(vertex, radians, numpy.array([0, 1, 0]), self.geometry_center)

    def rotate_z(self, radians: float):
        for index, vertex in enumerate(self._vertices):
            self._vertices[index] = rotate_vertex(vertex, radians, numpy.array([0, 0, 1]), self.geometry_center)
