import keyboard
import numpy


def handle_controls() -> numpy.ndarray:
    position_offset: numpy.ndarray = numpy.zeros(shape=(3,), dtype=int)
    control_steps: int = 5

    while True:
        input_received: bool = False

        if keyboard.is_pressed("a"):
            position_offset[2] -= control_steps
            input_received = True

        elif keyboard.is_pressed("d"):
            position_offset[2] += control_steps
            input_received = True

        if keyboard.is_pressed("w"):
            position_offset[1] += control_steps
            input_received = True

        elif keyboard.is_pressed("s"):
            position_offset[1] -= control_steps
            input_received = True

        if keyboard.is_pressed("shift"):
            position_offset[0] -= control_steps
            input_received = True

        elif keyboard.is_pressed("space"):
            position_offset[0] += control_steps
            input_received = True

        if input_received:
            break

    return position_offset
