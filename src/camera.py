import numpy

from src import terminal_size


class Camera:
    def __init__(
        self,
        position: numpy.ndarray,
        orientation: numpy.ndarray,
        viewing_frustum_planes: tuple[float, float],
        fov: float,
    ) -> None:
        self._position: numpy.ndarray = position
        self._orientation: numpy.ndarray = orientation
        self._distance_near_plane: float = viewing_frustum_planes[0]
        self._distance_far_plane: float = viewing_frustum_planes[1]
        self._field_of_view: float = numpy.deg2rad(fov)

    # def rotate(self, theta: tuple[float, float, float]) -> None:
    #     self._orientation += numpy.array(theta)

    @property
    def orientation(self) -> numpy.ndarray:
        return self._orientation

    @property
    def position(self) -> numpy.ndarray:
        return self._position

    def translate(self, delta: tuple[float, float, float]) -> None:
        self._position += numpy.array(delta)

    def project(
        self,
        vertex: numpy.ndarray,
    ) -> numpy.ndarray:
        a: float = terminal_size.height / terminal_size.width
        f: float = 1 / numpy.tan(self._field_of_view / 2)
        q: float = self._distance_far_plane / (self._distance_far_plane - self._distance_near_plane)
        projection_matrix: numpy.ndarray = numpy.array(
            [
                [a * f, 0, 0, 0],
                [0, f, 0, 0],
                [0, 0, q, 1],
                [0, 0, -self._distance_near_plane * q, 0],
            ]
        )
        projected_vertex: numpy.ndarray = numpy.array([*(vertex - self._position), 1]) @ projection_matrix
        projected_vertex /= projected_vertex[2]
        projected_vertex += 1
        projected_vertex /= 2
        projected_vertex[0] *= terminal_size.width
        projected_vertex[1] *= terminal_size.height

        return numpy.round(projected_vertex).astype(int)
