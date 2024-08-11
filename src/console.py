import numpy


def print_frame(height: int, width: int):
    frame: str = "\033[H" + "╭" + "─" * (width - 2) + "╮"

    for viewport_y in range(height - 2):
        frame += "│" + " " * (width - 2) + "│"

    frame += "╰" + "─" * (width - 2) + "╯"

    print("\033[?25l" + frame, flush=True, end="")


def print_viewport(viewport: numpy.ndarray):
    iterator: numpy.nditer = numpy.nditer(numpy.flip(viewport, axis=0), flags=["multi_index"], order="C")

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
