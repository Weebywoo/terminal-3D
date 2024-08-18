import numpy

from src.mesh import Mesh
from src.screen import Screen
from src.timer import Timer


@Timer
def render(screen: Screen, meshes: list[Mesh], stats: dict):
    screen.clear()

    for mesh in meshes:
        for vertex in mesh.vertices:
            screen.draw_vertex(vertex)

        screen.draw_quad(mesh.vertices[:4])
        screen.draw_quad(mesh.vertices[4:])
        screen.draw_line(mesh.vertices[0], mesh.vertices[4])
        screen.draw_line(mesh.vertices[2], mesh.vertices[6])
        screen.draw_line(mesh.vertices[3], mesh.vertices[7])
        screen.draw_line(mesh.vertices[5], mesh.vertices[1])

    screen.add_ui(stats)
    screen.print_frame()


def main():
    screen: Screen = Screen()
    cube: Mesh = Mesh(
        vertices=[
            numpy.array([1, -1, -5]),
            numpy.array([1, -1, -3]),
            numpy.array([1, 1, -5]),
            numpy.array([1, 1, -3]),
            numpy.array([-1, -1, -5]),
            numpy.array([-1, -1, -3]),
            numpy.array([-1, 1, -5]),
            numpy.array([-1, 1, -3]),
        ],
        vertex_order=[0, 1, 2, 1, 3, 2, 2, 3, 6, 3, 7, 6],
    )

    while True:
        render(screen, meshes=[cube])
        cube.rotate((0.0, 0.0005, 0.0))


if __name__ == "__main__":
    main()
