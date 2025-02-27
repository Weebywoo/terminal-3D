import numpy
from matplotlib.collections import Collection
from matplotlib.quiver import Quiver
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Line3DCollection, Poly3DCollection

from src.types import AnimationFunction, Mesh, Canvas, Camera


def update_corners(corners: Line3DCollection, meshes: list[Mesh]) -> Line3DCollection:
    xs, ys, zs = [], [], []

    for mesh in meshes:
        for index, vertex in enumerate(mesh.vertices):
            xs.append(vertex[0])
            ys.append(vertex[1])
            zs.append(vertex[2])

    corners._offsets3d = xs, ys, zs

    return corners


def update_faces(faces: Poly3DCollection, meshes: list[Mesh]) -> Poly3DCollection:
    vertices: list[tuple[numpy.ndarray, numpy.ndarray, numpy.ndarray]] = []

    for mesh in meshes:
        for index, face in enumerate(mesh.faces):
            vertex_one: numpy.ndarray = mesh.vertices[face[0]]
            vertex_two: numpy.ndarray = mesh.vertices[face[1]]
            vertex_three: numpy.ndarray = mesh.vertices[face[2]]

            vertices.append((vertex_one, vertex_two, vertex_three))

    faces.set_verts(vertices)
    faces.do_3d_projection()

    return faces


def update_normals(axes: Axes3D, meshes: list[Mesh]) -> Quiver:
    xa, ya, za, u, v, w = [], [], [], [], [], []

    for mesh in meshes:
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

    return axes.quiver(xa, ya, za, u, v, w)


def update_camera() -> None: ...


def update_func(
    frame: int,
    axes: Axes3D,
    animation_func: AnimationFunction,
    meshes: list[Mesh],
    canvas: Canvas,
    camera: Camera,
    corners: Line3DCollection,
    faces: Poly3DCollection,
) -> tuple[Line3DCollection, Collection, Quiver]:
    animation_func(frame, meshes, canvas, camera)

    for collection in axes.collections:
        if isinstance(collection, Line3DCollection):
            collection.remove()

    return (
        update_corners(corners, meshes),
        update_faces(faces, meshes),
        update_normals(axes, meshes),
    )
