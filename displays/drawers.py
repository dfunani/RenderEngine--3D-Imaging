from random import uniform
from models.interfaces.responses import Response
from models.raytracer.renders import Raytracer
from models.objects.primitives import Sphere
from models.objects.vectors import Vector3Float, RGB
from models.scene.materials import Material

class Drawer:
    @staticmethod
    def drawSpheres(spheres: int = 5, filename="untitled_spheres", extension="ppm") -> bool:
        try:
            res: list = []
            for _ in range(spheres):
                res.append(
                    Sphere(
                        Vector3Float(
                            (uniform(-2.5, 2.5)),
                            (uniform(-2.5, 2.5)),
                            (uniform(-1.1, -5.0)),
                        ),
                        (uniform(0.1, 1.0)),
                        Material(
                            RGB(
                                (uniform(0.0, 1.0)),
                                (uniform(0.0, 1.0)),
                                (uniform(0.0, 1.0)),
                            )
                        ),
                    )
                )
            Raytracer().exportPrimitives(res, filename, extension)
            if len(res) == spheres:
                return Response.success
            else:
                return Response.warning
        except BaseException:
            return Response.error

    @staticmethod
    def drawColorGradient(filename="untitled_gradient", extension="ppm") -> bool:
        try:
            Raytracer().exportColorGradient(filename, extension)
            return Response.success
        except BaseException:
            return Response.error
