from models.objects.primitives import Sphere
from models.objects.vectors import RGB, Vector3Float
from models.raytracer.renders import Raytracer

def test_raytracer():
    raytracer = Raytracer()
    raytracer.background_color = RGB(1.0, 1.0, 1.0)
    assert isinstance(raytracer.background_color, RGB)
    assert len(raytracer.background_color.coordinates) == 3
    assert all(raytracer.background_color.coordinates[i] == 1.0 for i in range(3))


def test_trace():
    raytracer = Raytracer()
    r = raytracer.trace(
        Vector3Float(0, 0, 0),
        Vector3Float(-1679.259456342853, 1679.259456342853, -1).normalize(),
        [Sphere(), Sphere(), Sphere()],
    )
    assert isinstance(r, RGB)
