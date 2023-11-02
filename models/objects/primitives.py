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
        pt: Vector3Float = Vector3Float()
        N: Vector3Float = Vector3Float()
        material: Material = Material(RGB())

        nearest_dist: float = 1e10
        if abs(rayDirection.coordinates[1]) > 0.001:
            d: float = (
                -(originalRayDirection.coordinates[1] + 4) / rayDirection.coordinates[1]
            )
            p: Vector3Float = (originalRayDirection + rayDirection) * d
            if (
                d > 0.001
                and d < nearest_dist
                and abs(p.coordinates[0]) < 10
                and p.coordinates[2] < -10
                and p.coordinates[2] > -30
            ):
                nearest_dist = d
                pt = p
                N = Vector3Float(0, 1, 0)
                material.color = (
                    RGB(0.3, 0.3, 0.3)
                    if (
                        int(0.5 * pt.coordinates[0] + 1000)
                        + int(0.5 * pt.coordinates[2])
                    )
                    & 1
                    else RGB(0.3, 0.2, 0.1)
                )

        for object in objects:
            intersect: dict = object.ray_intersect(originalRayDirection, rayDirection)
            if not intersect.get("result") or intersect.get("dist_i") > nearest_dist:
                continue
            nearest_dist = intersect.get("dist_i")
            pt = originalRayDirection + rayDirection * nearest_dist
            N = (pt - object.center).normalize()
            material = object.material
        return {"result": nearest_dist < 1000, "point": pt, "N": N, "material": material}


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
            return {"dist_i": 0, "result": False}

        thc: float = sqrt(self.squareRadius - squareDistance)
        dist_i = tca - thc
        dist_i_2 = tca + thc

        if dist_i > 0.001:
            return {"dist_i": dist_i, "result": True}
        if dist_i_2 > 0.001:
            return {"dist_i": dist_i_2, "result": True}

        # The previous conditions checked for non-intersection. If none of them was met, there is an intersection.
        return {"dist_i": dist_i, "result": False}
