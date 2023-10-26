from models.objects.vectors import (
    Vector,
    Vector2Float,
    Vector3Float,
    Vector3Int,
    Vector4Float,
    RGB,
)


def test_vectors():
    vector = Vector(0, 0, 0)
    assert len(vector.coordinates) == 3


def test_vectors_rgb():
    rgb = RGB()
    assert isinstance(rgb, Vector)
    assert len(rgb.coordinates) == 3


def test_vectors_vector2float():
    vector2float = Vector2Float()
    assert isinstance(vector2float, Vector)
    assert len(vector2float.coordinates) == 2


def test_vectors_vector3float():
    vector3float = Vector3Float()
    assert isinstance(vector3float, Vector)
    assert len(vector3float.coordinates) == 3


def test_vectors_vector3int():
    vector3int = Vector3Int()
    assert isinstance(vector3int, Vector)
    assert len(vector3int.coordinates) == 3


def test_vectors_vector4float():
    vector4float = Vector4Float()
    assert isinstance(vector4float, Vector)
    assert len(vector4float.coordinates) == 4
