import numpy
from scipy.spatial.transform import Rotation


def rotate_vertex(
    vertex: numpy.ndarray, radians: float, axis: numpy.ndarray, center_of_rotation: numpy.ndarray
) -> numpy.ndarray:
    rotation_vector: numpy.ndarray = radians * axis
    rotation = Rotation.from_rotvec(rotation_vector)
    translated_vertex = vertex - center_of_rotation

    return rotation.apply(translated_vertex) + center_of_rotation


def calculate_2d_bounding_box(vertices: list[numpy.ndarray]) -> tuple[numpy.ndarray, numpy.ndarray]:
    vertices: numpy.ndarray = numpy.asarray(vertices)
    y_axis: numpy.ndarray = vertices[1, :]
    x_axis: numpy.ndarray = vertices[2, :]
    y_min: numpy.ndarray = y_axis.min()
    y_max: numpy.ndarray = y_axis.max()
    x_min: numpy.ndarray = x_axis.min()
    x_max: numpy.ndarray = x_axis.max()

    return numpy.array([x_min, y_min], dtype=int), numpy.array([x_max, y_max], dtype=int)


def calculate_boundary_box(vertices: list[numpy.ndarray]) -> tuple[numpy.ndarray, numpy.ndarray]:
    vertices: numpy.ndarray = numpy.asarray(vertices)
    x_axis: numpy.ndarray = vertices[2, :]
    y_axis: numpy.ndarray = vertices[1, :]
    z_axis: numpy.ndarray = vertices[0, :]
    x_min: numpy.ndarray = x_axis.min()
    x_max: numpy.ndarray = x_axis.max()
    y_min: numpy.ndarray = y_axis.min()
    y_max: numpy.ndarray = y_axis.max()
    z_min: numpy.ndarray = z_axis.min()
    z_max: numpy.ndarray = z_axis.max()

    return numpy.array([x_min, y_min, z_min]), numpy.array([x_max, y_max, z_max])


def translate_vertex_around_camera(
    vertex: numpy.ndarray, camera_position: numpy.ndarray, camera_orientation: numpy.ndarray
) -> tuple[float, float]:
    rotation: Rotation = Rotation.from_rotvec(camera_orientation * numpy.pi / 2)

    return rotation.apply(vertex - camera_position).tolist()
