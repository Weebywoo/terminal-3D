import itertools
import time
from functools import partial
from typing import Optional

import numpy
from matplotlib import pyplot as plt, animation
from matplotlib.animation import FuncAnimation
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Text3D, Line3DCollection

from src.plot_animation_setup import update_func
from src.types import AnimationFunction, Mesh, Camera, Canvas


class RenderingEngine3D:
    def __init__(
        self,
        meshes: list[Mesh],
        camera: Camera,
        canvas: Canvas,
        fps: float,
        animation_func: Optional[AnimationFunction] = None,
    ) -> None:
        self._meshes: list[Mesh] = meshes
        self._camera: Camera = camera
        self._canvas: Canvas = canvas
        self._frames_per_second: float = fps
        self._animation_func: Optional[AnimationFunction] = animation_func

    def _project_meshes(self) -> None:
        for mesh in self._meshes:
            for index, face in enumerate(mesh.faces):
                projected_face: list[numpy.ndarray] = [
                    self._camera.project(mesh.vertices[face[0]]),
                    self._camera.project(mesh.vertices[face[1]]),
                    self._camera.project(mesh.vertices[face[2]]),
                ]

                triangle_center: numpy.ndarray = numpy.average(
                    [
                        mesh.vertices[face[0]],
                        mesh.vertices[face[1]],
                        mesh.vertices[face[2]],
                    ],
                    axis=0,
                )
                normal: numpy.ndarray = mesh.normals[index]

                if (
                    normal[0] * (triangle_center[0] - self._camera.position[0])
                    + normal[1] * (triangle_center[1] - self._camera.position[1])
                    + normal[2] * (triangle_center[2] - self._camera.position[2])
                    >= 0.0
                ):
                    continue

                self._canvas.draw_line(projected_face[0], projected_face[1])
                self._canvas.draw_line(projected_face[1], projected_face[2])
                self._canvas.draw_line(projected_face[2], projected_face[0])

    def start(self) -> None:
        frame_time: float = 1000 / self._frames_per_second

        for index in itertools.count():
            start_time: float = time.time()

            self._canvas.clear()

            if self._animation_func:
                self._animation_func(index, self._meshes, self._canvas, self._camera)

            self._project_meshes()
            self._canvas.draw()

            end_time: float = time.time()

            time.sleep(max(frame_time, end_time - start_time) / 1000)

    def visualise(self, save: bool = False) -> None:
        figure: Figure = plt.figure()
        axes: Axes3D = figure.add_subplot(projection="3d")
        xs, ys, zs = [], [], []

        for mesh in self._meshes:
            for index, vertex in enumerate(mesh.vertices):
                xs.append(vertex[0])
                ys.append(vertex[1])
                zs.append(vertex[2])

        corners: Line3DCollection = axes.scatter(xs, ys, zs)

        vertices: list[tuple[numpy.ndarray, numpy.ndarray, numpy.ndarray]] = []

        for mesh in self._meshes:
            for index, face in enumerate(mesh.faces):
                vertex_one: numpy.ndarray = mesh.vertices[face[0]]
                vertex_two: numpy.ndarray = mesh.vertices[face[1]]
                vertex_three: numpy.ndarray = mesh.vertices[face[2]]

                vertices.append((vertex_one, vertex_two, vertex_three))

        faces: Poly3DCollection = Poly3DCollection(vertices, shade=True, edgecolors="red", facecolors="#0000FF60")
        axes.add_collection3d(faces)

        xa, ya, za, u, v, w = [], [], [], [], [], []

        for mesh in self._meshes:
            for index, face in enumerate(mesh.faces):
                vertex_one: numpy.ndarray = mesh.vertices[face[0]]
                vertex_two: numpy.ndarray = mesh.vertices[face[1]]
                vertex_three: numpy.ndarray = mesh.vertices[face[2]]
                average: numpy.ndarray = numpy.average([vertex_one, vertex_two, vertex_three], axis=0)

                xa.append(average[0])
                ya.append(average[1])
                za.append(average[2])

                u.append(mesh.normals[index][0])
                v.append(mesh.normals[index][1])
                w.append(mesh.normals[index][2])

        axes.quiver(xa, ya, za, u, v, w)

        axes.scatter([self._camera.position[0]], [self._camera.position[2]], [self._camera.position[1]], marker="^")

        if self._animation_func is None:
            texts: list[Text3D] = []

            for mesh in self._meshes:
                for index, vertex in enumerate(mesh.vertices):
                    texts.append(axes.text3D(*vertex, s=f"{tuple(map(lambda a: round(a, 2), vertex.tolist()))}"))

        if self._animation_func is not None:
            func_animation = FuncAnimation(
                fig=figure,
                func=partial(
                    update_func,
                    axes=axes,
                    animation_func=self._animation_func,
                    meshes=self._meshes,
                    canvas=self._canvas,
                    camera=self._camera,
                    corners=corners,
                    faces=faces,
                ),
                interval=1000 / 60,
            )

        axes.set_aspect("equal")
        axes.set_xlabel("X")
        axes.set_ylabel("Z")
        axes.set_zlabel("Y")
        plt.show()

        if self._animation_func is not None and save:
            func_animation.save("./animation.gif", writer=animation.PillowWriter(fps=60))
