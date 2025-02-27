import numpy


class Mesh:
    def __init__(self, vertices: list[numpy.ndarray], faces: list[tuple[int, int, int]]):
        self._vertices: list[numpy.ndarray] = vertices
        self._faces: list[tuple[int, int, int]] = faces
        self._center: numpy.ndarray = numpy.average(vertices, axis=0)
        self._normals: list[numpy.ndarray] = self._update_normals()

    @property
    def vertices(self) -> list[numpy.ndarray]:
        return self._vertices

    @property
    def faces(self) -> list[tuple[int, int, int]]:
        return self._faces

    @property
    def normals(self) -> list[numpy.ndarray]:
        return self._normals

    @property
    def center(self) -> numpy.ndarray:
        return self._center

    def scale(self, factor: float) -> None:
        for index, vertex in enumerate(self._vertices):
            direction: numpy.ndarray = vertex - self._center
            self.vertices[index] = direction * factor - self._center

    def translate(self, translation: tuple[float, float, float]) -> None:
        translation: numpy.ndarray = numpy.array(translation)

        for vertex in self._vertices:
            vertex += translation

        self._center += translation

    def _update_normals(self) -> list[numpy.ndarray]:
        normals: list[numpy.ndarray] = []

        for face in self._faces:
            normal: numpy.ndarray = numpy.cross(
                self._vertices[face[2]] - self._vertices[face[0]], self._vertices[face[1]] - self._vertices[face[0]]
            )
            normal_magnitude: float = numpy.linalg.norm(normal).astype(float)

            if normal_magnitude > 0:
                normal /= normal_magnitude

            normals.append(normal)

        return normals

    def rotate(self, theta: tuple[float, float, float]) -> None:
        self._rotate_x(theta[0])
        self._rotate_y(theta[1])
        self._rotate_z(theta[2])

        self._normals = self._update_normals()

    def _rotate_x(self, theta: float) -> None:
        for index, vertex in enumerate(self._vertices):
            rotation_matrix: numpy.ndarray = numpy.array(
                [[1, 0, 0], [0, numpy.cos(theta), -numpy.sin(theta)], [0, numpy.sin(theta), numpy.cos(theta)]]
            )
            vertex: numpy.ndarray = numpy.swapaxes([vertex - self._center], 0, 1)

            self._vertices[index] = numpy.swapaxes(rotation_matrix @ vertex, 1, 0)[0] + self._center

    def _rotate_y(self, theta: float) -> None:
        for index, vertex in enumerate(self._vertices):
            rotation_matrix: numpy.ndarray = numpy.array(
                [[numpy.cos(theta), 0, numpy.sin(theta)], [0, 1, 0], [-numpy.sin(theta), 0, numpy.cos(theta)]]
            )
            vertex: numpy.ndarray = numpy.swapaxes([vertex - self._center], 0, 1)

            self._vertices[index] = numpy.swapaxes(rotation_matrix @ vertex, 1, 0)[0] + self._center

    def _rotate_z(self, theta: float) -> None:
        for index, vertex in enumerate(self._vertices):
            rotation_matrix: numpy.ndarray = numpy.array(
                [[numpy.cos(theta), -numpy.sin(theta), 0], [numpy.sin(theta), numpy.cos(theta), 0], [0, 0, 1]]
            )
            vertex: numpy.ndarray = numpy.swapaxes([vertex - self._center], 0, 1)

            self._vertices[index] = numpy.swapaxes(rotation_matrix @ vertex, 1, 0)[0] + self._center
