from math import tan, pi, sqrt
from models.constants import Resolution, Buffers
from models.objects.vectors import Vector3Float, Vector, RGB
from models.files.filemanagers import FileManager
from numpy.typing import NDArray
from typing import Any
from numpy.linalg import norm
from models.objects.primitives import Object
from models.objects.materials import Material
import random

class Raytracer:
    FOV: float = pi / 2.0
    __BACKGROUND_COLOR__: RGB = RGB(0.0, 0.0, 0.8)

    @property
    def background_color(self):
        return Raytracer.__BACKGROUND_COLOR__

    @background_color.setter
    def background_color(self, value):
        if not isinstance(value, RGB):
            raise TypeError("Color must be RGB")
        Raytracer.__BACKGROUND_COLOR__ = value

    def trace(
        self,
        rayOriginalDirection: Vector,
        rayDirection: Vector,
        objects: Object,
    ) -> Vector:
        scene: dict = Object.scene_intersect(
            rayOriginalDirection, rayDirection, objects
        )
        if not scene["result"]:
            Raytracer.background_color = RGB(
                (random.uniform(0.0, 0.1)),
                (random.uniform(0.0, 0.1)),
                (random.uniform(0.0, 1.0)),
            )
            return Raytracer.background_color
        return scene["material"].color

    def exportColorGradient(
        self, filename: str = "untitled", extension: str = "ppm"
    ) -> None:
        framebuffer: list[Vector3Float] = Buffers.frameBuffer()

        for j in range(Resolution.__HEIGHT__):
            for i in range(Resolution.__WIDTH__):
                framebuffer[i + j * Resolution.__WIDTH__] = Vector3Float(
                    (j) / float(Resolution.__HEIGHT__),
                    (i) / float(Resolution.__WIDTH__),
                    0.0,
                )

        FileManager(filename, extension).write(framebuffer)

    def exportPrimitives(
        self, objects: Object, filename: str = "untitled", extension: str = "ppm"
    ) -> None:
        framebuffer: list[Vector3Float] = Buffers.frameBuffer()

        for j in range(Resolution.__HEIGHT__):
            for i in range(Resolution.__WIDTH__):
                x: float = (
                    (2 * (i + 0.5) / float(Resolution.__WIDTH__) - 1)
                    * tan(Raytracer.FOV / 2.0)
                    * float(Resolution.__WIDTH__)
                    / float(Resolution.__HEIGHT__)
                )
                y: float = -(2 * (j + 0.5) / float(Resolution.__HEIGHT__) - 1) * tan(
                    Raytracer.FOV / 2.0
                )
                rayDirection: Vector3Float = Vector3Float(x, y, -1).normalize()
                framebuffer[i + j * Resolution.__WIDTH__] = self.trace(
                    Vector3Float(0, 0, 0), rayDirection, objects
                )

        FileManager(filename, extension).write(framebuffer)
