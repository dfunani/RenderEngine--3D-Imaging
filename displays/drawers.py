from random import uniform
from models.interfaces.responses import Response
from models.raytracer.renders import Raytracer
from models.objects.primitives import Sphere
from models.objects.vectors import Vector3Float, Vector4Float, RGB
from models.scene.lighting import Lighting
from models.scene.materials import Material
from logging import error
from traceback import print_exc


class Drawer:
    @staticmethod
    def drawSpheres(
        spheres: int = 5,
        filename="untitled_spheres",
        extension="ppm",
        lights=[
            Lighting(
                Vector3Float(
                    (uniform(-50, 50)),
                    (uniform(-50, 50)),
                    (uniform(-50, 50)),
                ),
                (uniform(0.0, 2.0)),
            )
            for _ in range(3)
        ],
    ) -> bool:
        try:
            res: list = []
            for _ in range(spheres):
                res.append(
                    Sphere(
                        Vector3Float(
                            (uniform(-10, 10)),
                            (uniform(-10, 10)),
                            (uniform(-1.0, -20.0)),
                        ),
                        (uniform(0.1, 4.0)),
                        Material(
                            RGB(
                                (uniform(0.0, 1.0)),
                                (uniform(0.0, 1.0)),
                                (uniform(0.0, 1.0)),
                            ),
                            Vector4Float(
                                (uniform(0.0, 1.0)),
                                (uniform(0.0, 1.0)),
                                (uniform(0.0, 1.0)),
                                (uniform(0.0, 0.0)),
                            ),
                            uniform(0.0, 1500.0),
                            uniform(0.0, 2.0),
                        ),
                    )
                )
            Raytracer().exportPrimitives(
                res,
                lights,
                filename,
                extension,
            )
            if len(res) == spheres:
                return Response.success
            else:
                error("Spheres Drawn: " + str(len(res)) + "/" + str(spheres))
                return Response.warning
        except BaseException as e:
            error("Draw Spheres: " + str(e))
            print_exc()
            return Response.error

    @staticmethod
    def drawColorGradient(filename="untitled_gradient", extension="ppm") -> bool:
        try:
            Raytracer().exportColorGradient(filename, extension)
            return Response.success
        except BaseException as e:
            error("Color-Gradient: " + str(e))
            print_exc()
            return Response.error

    @staticmethod
    def drawLightEmission(filename="untiled_light_image", extension="ppm"):
        try:
            ivory: Material = Material(
                RGB(0.4, 0.4, 0.3), Vector4Float(0.6, 0.3, 0.1, 0.0), 50.0, 1.0
            )
            glass: Material = Material(
                RGB(0.6, 0.7, 0.8),
                Vector4Float(0.0, 0.5, 0.1, 0.8),
                125.0,
                1.5,
            )
            red_rubber: Material = Material(
                RGB(0.3, 0.1, 0.1), Vector4Float(0.9, 0.1, 0.0, 0.0), 10.0, 1.0
            )
            mirror: Material = Material(
                RGB(1.0, 1.0, 1.0),
                Vector4Float(0.0, 10.0, 0.8, 0.0),
                1425.0,
                1.0,
            )

            spheres: list = []
            spheres.append(
                Sphere(
                    Vector3Float(-3, 0, -16),
                    2,
                    ivory,
                )
            )
            spheres.append(
                Sphere(
                    Vector3Float(-1.0, -1.5, -12),
                    2,
                    glass,
                )
            )
            spheres.append(
                Sphere(
                    Vector3Float(-5.0, -1.5, -12),
                    2,
                    ivory,
                )
            )
            spheres.append(
                Sphere(
                    Vector3Float(-5.0, 5.0, -12),
                    2,
                    red_rubber,
                )
            )
            spheres.append(
                Sphere(
                    Vector3Float(1.5, -0.5, -18),
                    3,
                    red_rubber,
                )
            )
            spheres.append(
                Sphere(
                    Vector3Float(7, 5, -18),
                    4,
                    mirror,
                )
            )
            lights: list = []
            lights.append(Lighting(Vector3Float(-20, 20, 20), 1.5))
            lights.append(Lighting(Vector3Float(30, 50, -25), 1.8))
            lights.append(Lighting(Vector3Float(30, 20, 30), 1.7))

            Raytracer().exportPrimitives(spheres, lights, filename, extension)
            return Response.success
        except BaseException as e:
            error("Light-Emission: " + str(e))
            print_exc()
            Response.error
