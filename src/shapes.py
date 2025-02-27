import numpy

from src.mesh import Mesh

vertices: list[numpy.ndarray] = [
    numpy.array([-0.5, -0.5, -0.5]),
    numpy.array([-0.5, 0.5, -0.5]),
    numpy.array([0.5, -0.5, -0.5]),
    numpy.array([0.5, 0.5, -0.5]),
    numpy.array([-0.5, -0.5, 0.5]),
    numpy.array([-0.5, 0.5, 0.5]),
    numpy.array([0.5, -0.5, 0.5]),
    numpy.array([0.5, 0.5, 0.5]),
]
faces: list[tuple[int, int, int]] = [
    (1, 2, 3),
    (7, 3, 2),
    (7, 2, 6),
    (5, 7, 6),
    (5, 6, 4),
    (1, 5, 4),
    (1, 4, 0),
    (6, 2, 4),
    (3, 7, 5),
    (0, 4, 2),
    (1, 3, 5),
    (0, 2, 1),
]


def cubes(amount: int) -> list[Mesh]:
    return [Mesh(vertices=vertices.copy(), faces=faces.copy()) for _ in range(amount)]
