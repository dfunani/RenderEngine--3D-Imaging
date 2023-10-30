from math import sqrt
from models.objects.vectors import Vector3Float, RGB
from models.scene.lighting import Lighting
from models.scene.materials import Material
from sys import float_info
from models.interfaces.constants import Resolution


class Object:
    def __init__(self, material: Material):
        if not isinstance(material, Material):
            raise TypeError("material must be of type Material")
        self.material: Material = material

    @staticmethod
    def reflect(I: Vector3Float, N: Vector3Float) -> Vector3Float:
        return I - N * 2.0 * (I * N)

    @staticmethod
    def refract(
        I: Vector3Float, N: Vector3Float, eta_t: float, eta_i: float = 1.0
    ) -> Vector3Float:
        cosi: float = -max(-1.0, min(1.0, I.dot(N)))
        if cosi < 0:
            return Object.refract(I, -N, eta_i, eta_t)

        eta: float = eta_i / eta_t
        k: float = 1 - eta * eta * (1 - cosi * cosi)
        return Vector3Float(1, 0, 0) if k < 0 else I * eta + N * (eta * cosi - sqrt(k))

    @staticmethod
    def frameBuffer(width=Resolution.__WIDTH__, height=Resolution.__HEIGHT__) -> list:
        return [Vector3Float() for _ in range(width * height)]

    @staticmethod
    def scene_intersect(
        originalRayDirection: Vector3Float, rayDirection: Vector3Float, objects: list
    ) -> dict:
        objects_dist: float = float_info.max
        result: dict = {}
        for object in objects:
            intersect = object.ray_intersect(originalRayDirection, rayDirection)
            if intersect and intersect.get("dist_i") < objects_dist:
                objects_dist = intersect.get("dist_i")
                result = {
                    "point": originalRayDirection + rayDirection * objects_dist,
                    "N": (
                        result.get("point", Vector3Float()) - object.center
                    ).normalize(),
                    "material": object.material,
                }
        checkerboard_dist: float = float_info.max
        if abs(rayDirection.coordinates[1]) > 1e-3:
            d: float = (
                -(originalRayDirection.coordinates[1] + 4) / rayDirection.coordinates[1]
            )
            pt: Vector3Float = originalRayDirection + rayDirection * d
            if (
                d > 0
                and abs(pt.coordinates[1]) < 10
                and pt.coordinates[2] < -10
                and pt.coordinates[2] > -30
                and d < objects_dist
            ):
                checkerboard_dist = d
                material = Material(RGB())
                material.color = (
                    Vector3Float(0.3, 0.3, 0.3)
                    if (int(0.5 * pt.coordinates[0] + 1000) + int(0.5 * pt.coordinates[2])) & 1
                    else Vector3Float(0.3, 0.2, 0.1)
                )
                result = {
                    "point": pt,
                    "N": Vector3Float(0, 1, 0),
                    "material": material,
                }
        return {**result, "result": min(objects_dist, checkerboard_dist) < 1000}


class Sphere(Object):
    def __init__(
        self,
        center: Vector3Float = Vector3Float(),
        radius: float = 1.0,
        material: Material = Material(RGB(0, 0, 0)),
    ) -> None:
        super().__init__(material)
        self.center: Vector3Float = center
        self.radius: float = radius
        self.squareRadius: float = radius**2

    def ray_intersect(
        self, originalRayDirection: Vector3Float, rayDirection: Vector3Float
    ) -> bool | dict:
        distance: Vector3Float = self.center - originalRayDirection
        tca: float = distance.dot(rayDirection)
        squareDistance: float = distance.dot(distance) - (tca * tca)

        if squareDistance > self.squareRadius:
            return False

        thc: float = sqrt(self.squareRadius - squareDistance)
        dist_i = tca - thc
        t1 = tca + thc

        if dist_i < 0:
            dist_i = t1

        if dist_i < 0:
            return False

        # The previous conditions checked for non-intersection. If none of them was met, there is an intersection.
        return {"dist_i": dist_i}
