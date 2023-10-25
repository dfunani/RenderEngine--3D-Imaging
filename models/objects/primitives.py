from math import sqrt
from typing import Any
from numpy.typing import NDArray
from models.objects.vectors import Vector3Float, RGB
from models.objects.materials import Material
from sys import float_info


class Object:
    def __init__(self, material: Material):
        self.material: Material = material

    @staticmethod
    def scene_intersect(
        originalRayDirection: Vector3Float,
        rayDirection: Vector3Float,
        objects: list,
    ) -> dict:
        objects_dist: float = float_info.max
        point: Vector3Float = Vector3Float()
        N: Vector3Float = Vector3Float()
        material: Material = RGB()
        result: dict = {}
        for object in objects:
            intersect = object.ray_intersect(originalRayDirection, rayDirection)
            if intersect and intersect["dist_i"] < objects_dist:
                objects_dist = intersect["dist_i"]
                result = {
                    "point": originalRayDirection + rayDirection * intersect["dist_i"],
                    "N": (point - object.center).normalize(),
                    "material": object.material,
                }

        return {**result, "result": objects_dist < 1000}


class Sphere(Object):
    def __init__(
        self,
        center: Vector3Float = Vector3Float(),
        radius: float = 1.0,
        material: Material = RGB(0, 0, 0),
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
