import itertools
import time

import numpy

from src.camera import Camera
from src.mesh import Mesh


def main():
    camera: Camera = Camera(position=numpy.array([0.0, 0.0, 0.0]), orientation=numpy.array([0.0, 0.0, 0.0]))
    cube: Mesh = Mesh(
        vertices=[
            numpy.array([-1.0, -1.0, -5.0]),
            numpy.array([1.0, -1.0, -5.0]),
            numpy.array([-1.0, -1.0, -3.0]),
            numpy.array([1.0, -1.0, -3.0]),
            numpy.array([-1.0, 1, -5]),
            numpy.array([1.0, 1.0, -5.0]),
            numpy.array([-1.0, 1.0, -3.0]),
            numpy.array([1.0, 1.0, -3.0]),
        ],
        vertex_order=[
            1,
            2,
            0,
            2,
            3,
            1,
            4,
            6,
            7,
            5,
            4,
            7,
            5,
            0,
            4,
            1,
            0,
            5,
            6,
            2,
            3,
            6,
            3,
            7,
            6,
            4,
            2,
            0,
            2,
            4,
            7,
            5,
            1,
            1,
            3,
            7,
        ],
    )
    meshes: list[Mesh] = [cube]
    target_frame_time: float = 1 / 30
    last_render_time: float = 0
    last_frame_time: float = 0

    for frame in itertools.count():
        iteration_start_time: float = time.time()

        # meshes[0].rotate((last_frame_time * 0.25, last_frame_time * 0.75, last_frame_time * 0.5))
        # camera.move((0.0, 0.0, last_frame_time * -1.0))
        camera.rotate((0.0, target_frame_time * 0.5, 0.0))
        camera.render(meshes, frame, last_frame_time, last_render_time, target_frame_time)

        render_end_time: float = time.time()
        last_render_time: float = render_end_time - iteration_start_time
        time_left_till_target_frame_time: float = target_frame_time - last_render_time

        if time_left_till_target_frame_time > 0.0:
            time.sleep(time_left_till_target_frame_time)

        frame_end_time: float = time.time()
        last_frame_time: float = frame_end_time - iteration_start_time


if __name__ == "__main__":
    main()
