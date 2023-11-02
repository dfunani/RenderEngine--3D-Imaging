from math import tan, pi
from models.interfaces.constants import Resolution
from models.objects.vectors import Vector3Float, Vector, RGB
from models.files.filemanagers import FileManager
from models.objects.primitives import Object
from random import uniform


class Raytracer:
    # FOV: float = pi / 3.0
    FOV: float = 1.05
    __BACKGROUND_COLOR__: RGB = RGB(0.2, 0.7, 0.8)

    @property
    def background_color(self):
        return self.__BACKGROUND_COLOR__

    @background_color.setter
    def background_color(self, value):
        if not isinstance(value, RGB):
            raise TypeError("Color must be RGB")
        Raytracer.__BACKGROUND_COLOR__ = value

    def ray_trace(
        self,
        rayOriginalDirection: Vector,
        rayDirection: Vector,
        objects: list,
        lights: list,
        depth: int = 0,
    ) -> Vector:
        scene: dict = Object.scene_intersect(
            rayOriginalDirection, rayDirection, objects
        )
        if depth > 4 or not scene.get("result"):
            return self.background_color

        diffuse_light_intensity: float = 0.0
        specular_light_intensity: float = 0.0
        reflect_dir: Vector3Float = Object.reflect(
            rayDirection, scene.get("N")
        ).normalize()
        refract_dir: Vector3Float = Object.refract(
            rayDirection, scene.get("N"), scene.get("material").refraction
        ).normalize()

        reflect_color: RGB = self.ray_trace(
            scene.get("point"), reflect_dir, objects, lights, depth + 1
        )
        refraction_color: RGB = self.ray_trace(
            scene.get("point"), refract_dir, objects, lights, depth + 1
        )
        for light in lights:
            light_dir: Vector3Float = (light.position - scene.get("point")).normalize()
            shadow_intersect: dict = Object.scene_intersect(
                scene.get("point"), light_dir, objects
            )

            if (
                shadow_intersect.get("result")
                and (shadow_intersect.get("point") - scene.get("point")).norm()
                < (light.position - scene.get("point")).norm()
            ):
                continue

            diffuse_light_intensity += light.intensity * max(
                0.0, light_dir.dot(scene.get("N"))
            )
            specular_light_intensity += pow(
                max(
                    0.0,
                    -Object.reflect(-light_dir, scene.get("N")).dot(rayDirection),
                ),
                scene.get("material").specular,
            )
        return (
            (
                scene.get("material").color
                * scene.get("material").albedo.coordinates[0]
                * diffuse_light_intensity
            )
            + (
                RGB(1.0, 1.0, 1.0)
                * scene.get("material").albedo.coordinates[1]
                * specular_light_intensity
            )
            + (reflect_color * scene.get("material").albedo.coordinates[2])
            + (refraction_color * scene.get("material").albedo.coordinates[3])
        )

    def exportColorGradient(
        self, filename: str = "untitled", extension: str = "ppm"
    ) -> None:
        framebuffer: list = Object.frameBuffer()

        for j in range(Resolution.__HEIGHT__):
            for i in range(Resolution.__WIDTH__):
                framebuffer[i + j * Resolution.__WIDTH__] = Vector3Float(
                    (j) / float(Resolution.__HEIGHT__),
                    (i) / float(Resolution.__WIDTH__),
                    0.0,
                )

        FileManager(filename, extension).write(framebuffer)

    def exportPrimitives(
        self,
        objects: list,
        lights: list,
        filename: str = "untitled",
        extension: str = "ppm",
    ) -> None:
        framebuffer: list = Object.frameBuffer()

        for pixel in range(Resolution.__WIDTH__ * Resolution.__HEIGHT__):
            dir_x: float = (
                pixel % Resolution.__WIDTH__ + 0.5
            ) - Resolution.__WIDTH__ / 2.0
            dir_y: float = (
                -(pixel / Resolution.__WIDTH__ + 0.5) + Resolution.__HEIGHT__ / 2.0
            )
            dir_z: float = -Resolution.__HEIGHT__ / (2.0 * tan(Raytracer.FOV / 2.0))
            rayDirection: Vector3Float = Vector3Float(dir_x, dir_y, dir_z).normalize()
            framebuffer[pixel] = self.ray_trace(
                Vector3Float(0, 0, 0), rayDirection, objects, lights
            )

        FileManager(filename, extension).write(framebuffer)
