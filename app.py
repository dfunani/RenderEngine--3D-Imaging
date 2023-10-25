from models.raytracer.renders import Raytracer
from models.objects.primitives import Sphere
from models.objects.vectors import Vector3Float, RGB
from models.objects.materials import Material
import random


def main():
    res: list = []
    for _ in range(5):
        res.append(
            Sphere(
                Vector3Float(
                    (random.uniform(-2.5, 2.5)),
                    (random.uniform(-2.5, 2.5)),
                    (random.uniform(-1.1, -5.0)),
                ),
                (random.uniform(0.1, 1.0)),
                Material(RGB((random.uniform(0.0, 1.0)),
                    (random.uniform(0.0, 1.0)),
                    (random.uniform(0.0, 1.0)),))
            )
        )
    Raytracer().exportPrimitives(res)


if __name__ == "__main__":
    main()
