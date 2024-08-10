import shutil

import numpy

from src import marchingcubes


def check_triangle_intersections(
    voxel: list,
    pixel_center: numpy.ndarray,
) -> tuple[numpy.ndarray, list] | None:
    for triangle in voxel:
        intersection: numpy.ndarray | None = ray_intersects_triangle(
            ray_origin=pixel_center,
            ray_vector=numpy.array([0.0, 1.0, 0.0]),
            triangle=triangle,
        )

        if intersection is None:
            continue

        return intersection, triangle

    return None


def get_marchingcubes_viewport(
    position: numpy.ndarray, viewport_size: tuple, max_depth: float
) -> numpy.ndarray:
    # figure: Figure = plt.figure()
    # axes_one = figure.add_subplot(1, 2, 2, projection="3d")
    # axes_two = figure.add_subplot(1, 2, 1)
    # triangles: list = []
    noise_scale: float = 15.0
    viewport: numpy.ndarray = numpy.full(shape=viewport_size, fill_value=1.0)

    for zi in numpy.arange(start=0, stop=viewport_size[0]):
        for xi in numpy.arange(start=0, stop=viewport_size[1]):
            pixel_center = position + (zi, 0.0, xi) + (0.5, 0.0, 0.5)

            for yi in numpy.arange(start=0, stop=max_depth):
                voxel_position = position + (zi, yi, xi)
                voxel: list | None = marchingcubes.voxel(
                    position=voxel_position, noise_scale=noise_scale
                )

                if voxel is None:
                    continue

                intersection: tuple | None = check_triangle_intersections(
                    voxel, pixel_center
                )

                if intersection is not None:
                    intersection_position, triangle = intersection
                    # triangles.append(triangle)
                    viewport[zi, xi] = numpy.linalg.norm(
                        intersection_position - pixel_center
                    )
                    viewport[zi, xi] /= max_depth
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


def cross(a: numpy.ndarray, b: numpy.ndarray) -> numpy.ndarray:
    return numpy.cross(a, b)


def ray_intersects_triangle(
    ray_origin: numpy.ndarray, ray_vector: numpy.ndarray, triangle: list[numpy.ndarray]
) -> numpy.ndarray | None:
    epsilon = 0.000001
    edge1 = triangle[1] - triangle[0]
    edge2 = triangle[2] - triangle[0]
    ray_cross_e2 = cross(ray_vector, edge2)
    det = numpy.dot(edge1, ray_cross_e2)

    if -epsilon < det < epsilon:
        return None

    inv_det = 1.0 / det
    s = ray_origin - triangle[0]
    u = inv_det * numpy.dot(s, ray_cross_e2)

    if u < 0 or u > 1:
        return None

    s_cross_e1 = cross(s, edge1)
    v = inv_det * numpy.dot(ray_vector, s_cross_e1)

    if v < 0 or u + v > 1:
        return None

    # At this stage we can compute t to find out where the intersection point is on the line.
    t = inv_det * numpy.dot(edge2, s_cross_e1)

    if t > epsilon:
        return ray_origin + ray_vector * t

    return None


def print_frame(height: int, width: int):
    frame: str = "╭" + "─" * (width - 2) + "╮"

    for viewport_y in range(height - 2):
        frame += "│" + " " * (width - 2) + "│"

    frame += "╰" + "─" * (width - 2) + "╯"

    print("\033[?25l" + frame, flush=True, end="")


def main():
    terminal_size = shutil.get_terminal_size()
    width, height = terminal_size.columns, terminal_size.lines
    position: numpy.ndarray = numpy.array([0, 0, 0])
    size = (height - 2, (width - 4) // 2)
    print_frame(height, width)
    max_depth: float = 15.0
    viewport: numpy.ndarray = get_marchingcubes_viewport(position, size, max_depth)
    iterator: numpy.nditer = numpy.nditer(
        numpy.flip(viewport, axis=0), flags=["multi_index"], order="C"
    )

    for item in iterator:
        line, column = iterator.multi_index
        cursor_position: str = f"\033[{line + 2};{column * 2 + 3}H"
        gray_scale: int = int(255 * (1 - item))
        color: str = f"\033[38;2;{gray_scale};{gray_scale};{gray_scale}m"
        reset: str = "\033[m"

        if item:
            print(cursor_position + color + "██" + reset, end="", flush=True)

        else:
            print(cursor_position + color + "  " + reset, end="", flush=True)

    # plt.show()


if __name__ == "__main__":
    main()
