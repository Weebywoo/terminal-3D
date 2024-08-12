import numpy
from numba import njit

from src import marchingcubes
from src.constants import MAX_DEPTH


@njit
def ray_intersects_triangle(
    ray_origin: numpy.ndarray, ray_vector: numpy.ndarray, triangle: list[numpy.ndarray]
) -> numpy.ndarray | None:
    epsilon: float = 0.000001
    edge1: numpy.ndarray = triangle[1] - triangle[0]
    edge2: numpy.ndarray = triangle[2] - triangle[0]
    ray_cross_e2: numpy.ndarray = numpy.cross(ray_vector, edge2)
    det: numpy.ndarray = numpy.dot(edge1, ray_cross_e2)

    if -epsilon < det < epsilon:
        return None

    inv_det: numpy.ndarray = 1.0 / det
    s: numpy.ndarray = ray_origin - triangle[0]
    u: numpy.ndarray = inv_det * numpy.dot(s, ray_cross_e2)

    if u < 0 or u > 1:
        return None

    s_cross_e1: numpy.ndarray = numpy.cross(s, edge1)
    v: numpy.ndarray = inv_det * numpy.dot(ray_vector, s_cross_e1)

    if v < 0 or u + v > 1:
        return None

    # At this stage we can compute t to find out where the intersection point is on the line.
    t: float = inv_det * numpy.dot(edge2, s_cross_e1)

    if t > epsilon:
        return ray_origin + ray_vector * t

    return None


def get_marchingcubes_viewport(
    position: numpy.ndarray,
    viewport_size: tuple[int, int],
    voxel_storage: dict[tuple, list],
) -> numpy.ndarray:
    # figure: Figure = plt.figure()
    # axes_one = figure.add_subplot(1, 2, 2, projection="3d")
    # axes_two = figure.add_subplot(1, 2, 1)
    # triangles: list = []
    viewport: numpy.ndarray = numpy.full(shape=viewport_size, fill_value=1.0)

    for zi in numpy.arange(start=0, stop=viewport_size[0]):
        for xi in numpy.arange(start=0, stop=viewport_size[1]):
            pixel_center = position + (zi, 0.0, xi) + (0.5, 0.0, 0.5)

            for yi in numpy.arange(start=0, stop=MAX_DEPTH):
                voxel_position = position + (zi, yi, xi)
                z, y, x = voxel_position

                if (z, y, x) in voxel_storage:
                    triangles = voxel_storage[(z, y, x)]

                else:
                    triangles: list = marchingcubes.voxel(position=voxel_position)
                    voxel_storage[(z, y, x)] = triangles

                if len(triangles) == 0:
                    continue

                # triangles.extend(voxel)

                intersection: numpy.ndarray | None = check_triangle_intersections(triangles, pixel_center)

                if intersection is not None:
                    viewport[zi, xi] = intersection_distance(pixel_center, intersection)
                    break

    # marchingcubes.plot(position, viewport_size, max_depth, triangles, axes_one)
    # axes_one.set_aspect("equal")
    # axes_two.imshow(
    #     numpy.full(
    #         shape=viewport_size,
    #         fill_value=1.0
    #     ) - viewport,
    #     origin="lower",
    #     cmap='gray',
    #     vmin=0.0,
    #     vmax=1.0
    # )

    return viewport


@njit
def check_triangle_intersections(voxel: list, pixel_center: numpy.ndarray) -> numpy.ndarray | None:
    for triangle in voxel:
        intersection: numpy.ndarray | None = ray_intersects_triangle(
            ray_origin=pixel_center,
            ray_vector=numpy.array([0.0, 1.0, 0.0]),
            triangle=triangle,
        )

        if intersection is None:
            continue

        return intersection

    return None


@njit
def intersection_distance(pixel_center: numpy.ndarray, intersection: numpy.ndarray) -> float:
    return numpy.linalg.norm(intersection - pixel_center) / MAX_DEPTH
