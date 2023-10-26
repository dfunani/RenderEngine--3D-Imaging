from pytest import raises
from models.objects.vectors import RGB

from models.scene.materials import Material


def test_material():
    material = Material(RGB())
    assert len(material.color.coordinates) == 3
    assert all(material.color.coordinates[i] == 0.0 for i in range(3))
    with raises(TypeError):
        assert Material(1.0)
