import shutil
from os import terminal_size

_terminal_size: terminal_size = shutil.get_terminal_size()

height: int = _terminal_size.lines * 2
width: int = _terminal_size.columns
aspect_ratio: float = width / height
