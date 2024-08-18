import numpy


class Triangle:
    def __init__(self, vertices: list[numpy.ndarray]):
        self._vertices: list[numpy.ndarray] = vertices

    def __getitem__(self, index: int) -> numpy.ndarray:
        return self._vertices[index]

    @property
    def vertices(self) -> list[numpy.ndarray]:
        return self._vertices
