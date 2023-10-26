from models.objects.primitives import Object, Sphere
from models.objects.vectors import RGB
from models.scene.materials import Material
from models.interfaces.constants import Resolution
from models.objects.vectors import Vector3Float
from pytest import raises


def test_objects():
    object = Object(Material(RGB()))
    assert isinstance(object.material.color, RGB)
    with raises(TypeError):
        assert Object(RGB())


def test_objects_framebuffer():
    assert len(Object.frameBuffer()) == (Resolution.__WIDTH__ * Resolution.__HEIGHT__)
    assert all(isinstance(item, Vector3Float) for item in Object.frameBuffer())


def test_objects_sceneintersect():
    keys: list = ["point", "N", "material", "result"]
    originalRayDirection: Vector3Float = Vector3Float()
    rayDirection: Vector3Float = Vector3Float()
    objects: list = [Sphere(), Sphere()]
    intersect: dict = Object.scene_intersect(
        originalRayDirection,
        rayDirection,
        objects,
    )
    for key in intersect:
        assert key in keys
