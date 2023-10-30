from math import tan, pi
from models.interfaces.constants import Resolution
from models.objects.vectors import Vector3Float, Vector, RGB
from models.files.filemanagers import FileManager
from models.objects.primitives import Object
from random import uniform


class Raytracer:
    FOV: float = pi / 3.0
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
    ) -> RGB:
        scene: dict = Object.scene_intersect(
            rayOriginalDirection, rayDirection, objects
        )
        if depth > 4 or not scene.get("result"):
            # Raytracer.background_color = RGB(
            #     (uniform(0.0, 0.1)),
            #     (uniform(0.0, 0.1)),
            #     (uniform(0.0, 1.0)),
            # )
            return self.background_color

        diffuse_light_intensity: float = 0.0
        specular_light_intensity: float = 0.0
        reflect_dir: Vector3Float = Object.reflect(
            rayDirection, scene.get("N")
        ).normalize()
        refract_dir: Vector3Float = Object.refract(
            rayDirection, scene.get("N"), scene.get("material").refraction
        ).normalize()
        reflect_orig: Vector3Float = (
            (scene.get("point") - scene.get("N")) * 1e-3
            if reflect_dir * scene.get("N") < 0
            else (scene.get("point") + scene.get("N")) * 1e-3
        )
        refract_orig: Vector3Float = (
            (scene.get("point") - scene.get("N")) * 1e-3
            if refract_dir * scene.get("N") < 0
            else (scene.get("point") + scene.get("N")) * 1e-3
        )
        reflect_color: RGB = self.ray_trace(
            reflect_orig, reflect_dir, objects, lights, depth + 1
        )
        refraction_color: RGB = self.ray_trace(
            refract_orig, refract_dir, objects, lights, depth + 1
        )
        for light in lights:
            light_dir: Vector3Float = (light.position - scene.get("point")).normalize()
            light_distance: float = (light.position - scene.get("point")).norm()

            shadow_origin: Vector3Float = (
                scene.get("point") - scene.get("N") * 1e-3
                if light_dir * scene.get("N") < 0
                else scene.get("point") + scene.get("N") * 1e-3
            )
            shadow_intersect: dict = Object.scene_intersect(
                shadow_origin, light_dir, objects
            )

            if (
                shadow_intersect.get("result")
                and (shadow_intersect.get("point") - shadow_origin).norm()
                < light_distance
            ):
                continue

            diffuse_light_intensity += light.intensity * max(
                0.0, light_dir.dot(scene.get("N"))
            )
            specular_light_intensity += (
                pow(
                    max(
                        0.0,
                        -Object.reflect(-light_dir, scene.get("N")).dot(rayDirection),
                    ),
                    scene.get("material").specular,
                )
                * light.intensity
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

        for j in range(Resolution.__HEIGHT__):
            for i in range(Resolution.__WIDTH__):
                # x: float = (
                #     (2 * (i + 0.5) / float(Resolution.__WIDTH__) - 1)
                #     * tan(Raytracer.FOV / 2.0)
                #     * float(Resolution.__WIDTH__)
                #     / float(Resolution.__HEIGHT__)
                # )
                # y: float = -(2 * (j + 0.5) / float(Resolution.__HEIGHT__) - 1) * tan(
                #     Raytracer.FOV / 2.0
                # )
                dir_x: float = (i + 0.5) - Resolution.__WIDTH__ / 2.0
                dir_y: float = -(j + 0.5) + Resolution.__HEIGHT__ / 2.0
                dir_z: float = -Resolution.__HEIGHT__ / (2.0 * tan(Raytracer.FOV / 2.0))
                # rayDirection: Vector3Float = Vector3Float(x, y, -1).normalize()
                rayDirection: Vector3Float = Vector3Float(
                    dir_x, dir_y, dir_z
                ).normalize()
                pixel = self.ray_trace(
                    Vector3Float(0, 0, 0), rayDirection, objects, lights
                )
                framebuffer[i + j * Resolution.__WIDTH__] = pixel

        FileManager(filename, extension).write(framebuffer)
