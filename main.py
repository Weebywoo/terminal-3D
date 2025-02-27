import numpy

from src.camera import Camera
from src.canvas import Canvas
from src.mesh import Mesh
from src.rendering_engine_3d import RenderingEngine3D
from src.shapes import cubes


def main():
    def animation_func(index: int, meshes: list[Mesh], canvas: Canvas, camera: Camera) -> None:
        meshes[0].rotate((0.02, 0.0, 0.0))
        meshes[1].rotate((-0.02, 0.0, 0.0))

    meshes: list[Mesh] = cubes(2)

    meshes[0].scale(15.0)
    meshes[0].translate((-8.0, 0.0, 25.0))

    meshes[1].scale(15.0)
    meshes[1].translate((8.0, 0.0, 25.0))

    canvas: Canvas = Canvas()
    camera: Camera = Camera(
        position=numpy.array([0.0, 0.0, 0.0]),
        orientation=numpy.array([0.0, 0.0, 1.0]),
        viewing_frustum_planes=(1.0, 10.0),
        fov=90.0,
    )
    engine: RenderingEngine3D = RenderingEngine3D(
        meshes, camera=camera, canvas=canvas, animation_func=animation_func, fps=60
    )

    engine.start()


if __name__ == "__main__":
    main()
