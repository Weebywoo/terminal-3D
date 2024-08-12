import numpy

RESET: str = "\033[m"
BLACK_FG: str = "\033[30m"
WHITE_FG: str = "\033[37m"
BLACK_BG: str = "\033[40m"
FOREGROUND_CLR_TMPL: str = "\033[38;5;{}m{]"
BACKGROUND_CLR_TMPL: str = "\033[48;5;{}m"


def float2ansi(value: float) -> int:
    return 232 + int(round(24 * value))


def add_render(frame_buffer: numpy.ndarray, viewport: numpy.ndarray):
    viewport_iterator: numpy.nditer = numpy.nditer(viewport, flags=["multi_index"], order="C")

    for viewport_pixel in viewport_iterator:
        ansi_color: str = BACKGROUND_CLR_TMPL.format(float2ansi(1 - viewport_pixel)) + " "
        y, x = viewport_iterator.multi_index
        frame_buffer[y, x + x] = ansi_color
        frame_buffer[y, x + x + 1] = ansi_color


def add_ui(frame_buffer: numpy.ndarray, height: int, width: int, stats: dict):
    # Add frame
    for index, string in enumerate("╭" + "─" * (width - 2) + "╮"):
        frame_buffer[0, index] = string

    for viewport_y in range(1, height - 1):
        frame_buffer[viewport_y, 0] = RESET + "│"
        frame_buffer[viewport_y, 1] = " "
        frame_buffer[viewport_y, -2] = RESET + " "
        frame_buffer[viewport_y, -1] = "│"

    for index, string in enumerate("╰" + "─" * (width - 2) + "╯"):
        frame_buffer[-1, index] = string

    # Add stats
    longest_key = max(map(len, stats.keys()))
    longest_unit = max(map(lambda value: len(value[1]), stats.values()))
    frame_buffer[0, 23] = "┬"

    for index, (stat_name, (stat_value, stat_unit)) in enumerate(stats.items()):
        stat: str = f"{stat_name.ljust(longest_key)} {str(stat_value).rjust(5)} {stat_unit.ljust(longest_unit)}"

        add_text(frame_buffer, stat, (index + 1, 2))

        frame_buffer[index + 1, 22] = RESET + " "
        frame_buffer[index + 1, 23] = "│"
        frame_buffer[index + 1, 24] = " "

    for index, string in enumerate("├" + "─" * 22 + "╯ "):
        frame_buffer[len(stats) + 1, index] = string


def print_frame(frame_buffer: numpy.ndarray):
    stdout_buffer: str = "\033[H\033[?25l" + "".join(map(lambda line: "".join(line), frame_buffer))

    print(stdout_buffer, end="", flush=True)


def add_text(frame_buffer: numpy.ndarray, text: str, position: tuple[int, int]):
    for index, character in enumerate(text):
        frame_buffer[position[0], position[1] + index] = character
