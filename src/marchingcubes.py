import noise
import numpy
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

from src.constants import (
    SURFACE_LEVEL,
    NOISE_SCALE,
    EDGE_INDEX_TO_VERTEX_INDICES,
    TRIANGULATION_TABLE,
    VERTEX_INDICES,
)


def plot(position, viewport_size: tuple, max_depth, triangles: list, axes: Axes3D):
    for index, triangle in enumerate(triangles):
        triangle: list = list(map(lambda vertex: list(reversed(vertex)), triangle))
        collection: Poly3DCollection = Poly3DCollection(
            verts=[numpy.asarray(triangle)], shade=True, edgecolors="red", zorder=10
        )

        axes.add_collection3d(collection)

    axes.set_xlim3d(position[2], position[2] + viewport_size[1])
    axes.set_ylim3d(position[1], position[1] + max_depth)
    axes.set_zlim3d(position[0], position[0] + viewport_size[0])
    axes.set_xlabel("X")
    axes.set_ylabel("Y")
    axes.set_zlabel("Z")


def mean(vertex_one: tuple[int, int, int], vertex_two: tuple[int, int, int]) -> numpy.ndarray:
    return numpy.array(
        [
            (vertex_one[0] + vertex_two[0]) / 2,
            (vertex_one[1] + vertex_two[1]) / 2,
            (vertex_one[2] + vertex_two[2]) / 2,
        ]
    )


def _construct_triangle(edge_indices: list[int]) -> list[numpy.ndarray]:
    triangle: list[numpy.ndarray] = []

    for edge_index in edge_indices:
        index_one, index_two = EDGE_INDEX_TO_VERTEX_INDICES[edge_index]
        vertex: numpy.ndarray = mean(VERTEX_INDICES[index_one], VERTEX_INDICES[index_two])

        triangle.append(vertex)

    return triangle


def _construct_triangles(triangulation_index: int) -> list:
    edge_indices: list[int] = TRIANGULATION_TABLE[triangulation_index]
    triangles: list = []

    for index in range(0, len(edge_indices), 3):
        triangles.append(_construct_triangle(edge_indices[index : index + 3]))

    return triangles


def voxel(position: numpy.ndarray) -> list | None:
    noise_values: numpy.ndarray = _get_voxel_noise_simplex(position)
    surface_mask: numpy.ndarray = numpy.less(noise_values, numpy.full(noise_values.shape, SURFACE_LEVEL))
    triangulation_index: int = sum(
        2**index for index, (zi, yi, xi) in enumerate(VERTEX_INDICES) if surface_mask[zi, yi, xi]
    )

    if triangulation_index == 0 or triangulation_index == 255:
        return None

    triangles_in_cube: list = _construct_triangles(triangulation_index)
    triangles_in_cube += position

    return triangles_in_cube


def _get_voxel_noise_simplex(position: numpy.ndarray) -> numpy.ndarray:
    noise_values: numpy.ndarray = numpy.zeros(shape=(2, 2, 2))

    for z, y, x in VERTEX_INDICES:
        noise_values[z, y, x] = noise.snoise3(
            x=(x + position[2]) / NOISE_SCALE,
            y=(y + position[1]) / NOISE_SCALE,
            z=(z + position[0]) / NOISE_SCALE,
        )

    return noise_values
