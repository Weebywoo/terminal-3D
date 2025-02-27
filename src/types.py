from typing import TypeAlias, Callable

from src.camera import Camera
from src.canvas import Canvas
from src.mesh import Mesh

AnimationFunction: TypeAlias = Callable[[int, list[Mesh], Canvas, Camera], None]
