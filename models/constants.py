from typing import Any, Union
from numpy import array
from numpy.typing import NDArray
from enum import Enum
from models.objects.vectors import Vector3Float

class Resolution:
    __WIDTH__ = 1024
    __HEIGHT__ = 768

class Buffers:
    @classmethod
    def frameBuffer(cls, width=Resolution.__WIDTH__, height=Resolution.__HEIGHT__) -> list[Vector3Float]:
        return ["Vector3Float" for _ in range(width * height)]


